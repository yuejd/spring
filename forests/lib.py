import threading
import queue
import winrm
import json
import paramiko
from django.conf import settings
import os
import re
from forests.models import Switch


def get_server_info(server):
    info = []
    guess = queue.Queue()
    guess.put({
        'type': 'windows',
        'mount_point': 'k',
        'shared': '\\\\10.103.118.1\\linux\\NWC\\script\\windows',
        'shared_usr': 'linux',
        'shared_psw': 'linux',
        'script': 'Get-HBAWin.ps1'
        })
    guess.put({
        'type': 'linux',
        'script': 'linux_hba_info.sh',
        })

    def _get_info(task):
        if task['type'] == 'windows':
            s = winrm.Session(
                server.ip_addr,
                auth=(server.username, server.password)
                )
            try:
                # mount and execute the script
                # do not split these two actions cause the mount is only
                # available for this session
                r = s.run_ps(
                    'net use ' + task['mount_point'] + ': ' +
                    task['shared'] + ' /user:' +
                    task['shared_usr'] + ' ' + task['shared_psw'] + '; ' +
                    task['mount_point'] + ':\\' + task['script']
                    )
                # umount
                s.run_ps('net use ' + task['mount_point'] + ': /delete')
            except:
                # TODO put the exception detail into log
                return None
            if r.status_code == 0:
                json_str = r.std_out[r.std_out.find('['):r.std_out.find(']')+1]
                # fix a problem caused by winrm
                json_str = json_str.replace("\'b\'", "")
                return json.loads(json_str)

        elif task['type'] == 'linux':
            linux_sshc = paramiko.client.SSHClient()
            linux_sshc.set_missing_host_key_policy(
                paramiko.client.AutoAddPolicy()
                )
            try:
                linux_sshc.connect(
                    server.ip_addr,
                    username=server.username,
                    password=server.password
                    )
            except:
                # TODO put the exception detail into log
                return None
            (i, o, e) = linux_sshc.exec_command(
                open(os.path.join(
                    settings.SCRIPTS_DIR,
                    task['script']), 'r').read()
                )
            linux_info = o.read()
            if linux_info:
                linux_info = linux_info.decode('utf-8').replace(",\n]", "\n]")
                return json.loads(linux_info)
        return None

    def worker():
        while True:
            task = guess.get()
            new_info = threading.local()
            new_info.res = _get_info(task)
            if new_info.res:
                info.append(new_info.res)
            guess.task_done()

    for x in range(2):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    guess.join()
    return info


def _nodefind(switch, wwpns):
    connections = []
    sshc = paramiko.client.SSHClient()
    sshc.set_missing_host_key_policy(
        paramiko.client.AutoAddPolicy()
    )
    try:
        sshc.connect(
            switch.ip_addr,
            username=switch.username,
            password=switch.password
        )
    except:
        # TODO put the exception detail into log
        return None

    if switch.vendor == 'cisco':
        cmd = "show fcns database detail | grep -B 2 -A 14 "
        for wwpn in wwpns:
            (i, o, e) = sshc.exec_command(cmd + wwpn)
            info = o.read().decode('utf-8')
            if info:
                connections.append({
                    'WWPN': wwpn,
                    'SW_IP': re.search('(?<=\()\d+(\.\d+){3}', info).group(),
                    'Port': re.search(r'(?<=:).*(?=\nSwitch)', info).group(),
                    'VSAN': re.search(r'(?<=VSAN:)\d+', info).group()
                })
    elif switch.vendor == 'brocade':
        cmd = "nodefind "
        for wwpn in wwpns:
            (i, o, e) = sshc.exec_command(cmd + wwpn)
            info = o.read().decode('utf-8')
            if "No device found" not in info:
                temp = {
                    'WWPN': wwpn,
                    'Port': re.search(r'(?<=Port Index: )\w+', info).group()
                    }
                sw_id = re.search(r'\w{2}(?=\w{4};)', info).group()
                (i, o, e) = sshc.exec_command("switchshow")
                info = o.read().decode('utf-8')
                if info:
                    temp['VSAN'] = re.search(r'(?<=FID: )\d+', info).group()
                (i, o, e) = sshc.exec_command("fabricshow | grep fffc" + sw_id)
                info = o.read().decode('utf-8')
                if info:
                    temp['SW_IP'] = re.search('\d+(\.\d+){3}', info).group()
                    temp['SW_USR'] = switch.username
                    connections.append(temp)

    return connections


def get_connection_info(wwpns):
    info = []
    # ----switch queue setup start
    switches = queue.Queue()

    for entry in settings.NODEFIND_SCOPE:
        try:
            switches.put(
                Switch.objects.get(
                    ip_addr=entry.get('ip'),
                    username=entry.get('username')
                )
            )
        except Switch.DoesNotExist:
            # TODO add log
            pass

    # ----switch queue setup done

    def worker():
        while True:
            switch = switches.get()
            for item in _nodefind(switch, wwpns):
                info.append(item)
            switches.task_done()

    for x in range(20):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    switches.join()
    return info
