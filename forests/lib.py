import threading
import queue
import winrm
import json
import paramiko
from django.conf import settings
import os
import re
from forests.models import Switch

TIMEOUT = 10


def _linux_info_process(data):
    return json.loads(data.decode('utf-8').replace(",\n]", "\n]"))


def _esxi_info_process(data):
    temp = []
    for line in data.decode('utf-8').split("\n"):
        if 'fc.' in line:
            descript = re.search(r'(?<=\) ).*', line).group()
            if 'link-up' in line:
                active = True
            else:
                active = False
            wwpn = re.search(r'(?<=:)\w{16}', line).group()
            wwpn = ':'.join(
                a+b for a, b in zip(wwpn[::2], wwpn[1::2])
                )
            temp.append({
                'ModelDescription': descript,
                'Active': active,
                'WWPN': wwpn
                })
    return temp


def _solaris_info_process(data):
    return json.loads(data.decode('utf-8'))

def _hp_info_process(data):
    rtn = []
    lines = data.decode("utf-8").splitlines()
    lines_num = len(lines)
    for i in range(lines_num):
        lines[i] = lines[i].strip().strip('"')
    for i in range(int(lines_num / 5)):
        i=i*5
        wwn = lines[i][2:]
        rtn.append({
            "WWPN" : ":".join([x+y for x, y in zip(wwn[::2], wwn[1::2])]),
            "Active" : True if "ONLINE" in lines[i+1] else False,
            "ModelDescription" : lines[i+2],
            "SerialNumber" : lines[i+3],
            "FirmwareVersion" : lines[i+4],
            "Model" : "HP"
        })
    return rtn

def _aix_info_process(data):
    rtn = []
    lines = data.decode("utf-8").splitlines()
    lines_num = len(lines)
    for i in range(int(lines_num / 2)):
        i = i *2
        wwn = lines[i]
        rtn.append({
            "WWPN" : ":".join([x+y for x, y in zip(wwn[::2], wwn[1::2])]).lower(),
            "Active" : True,
            "ModelDescription" : lines[i+1]
            })
    return rtn


def get_server_info(server):
    info = []
    guess = queue.Queue()
    guess.put({
        'type': 'winrm',
        'mount_point': 'k',
        'shared': '\\\\10.103.118.1\\linux\\NWC\\script\\windows',
        'shared_usr': 'linux',
        'shared_psw': 'linux',
        'script': 'Get-HBAWin.ps1'
        })
    guess.put({
        'type': 'ssh',
        'cmd_template': "{}",
        'script': 'linux_hba_info.sh',
        'success': _linux_info_process,
        })
    guess.put({
        'type': 'ssh',
        'cmd_template': "perl -e '{} '",
        'script': 'solaris_hba_info.pl',
        'success': _solaris_info_process,
        })
    guess.put({
        'type': 'ssh',
        'cmd_template': "esxcfg-scsidevs -a",
        'success': _esxi_info_process,
        })
    # for hp
    guess.put({
        "type": "ssh",
        "cmd_template": "{}",
        "script": "hp_hba_info.sh",
        "success": _hp_info_process,
        })

    # for aix
    guess.put({
        "type": "ssh",
        "cmd_template": "{}",
        "script": "aix_hba_info.sh",
        "success": _aix_info_process,
        })

    def _get_info(task):
        if task['type'] == 'winrm':
            s = winrm.Session(
                server.ip_addr,
                auth=(server.username, server.password)
                )
            s.protocol.transport.timeout = TIMEOUT
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

        elif task['type'] == 'ssh':
            ssh_client = paramiko.client.SSHClient()
            ssh_client.set_missing_host_key_policy(
                paramiko.client.AutoAddPolicy()
                )
            try:
                ssh_client.connect(
                    server.ip_addr,
                    username=server.username,
                    password=server.password,
                    timeout=TIMEOUT
                    )
            except:
                # TODO put the exception detail into log
                return None

            if task.get('script'):
                cmd = task['cmd_template'].format(
                    open(
                        os.path.join(settings.SCRIPTS_DIR, task['script']),
                        'r'
                    ).read()
                )
            else:
                cmd = task['cmd_template']

            (i, o, e) = ssh_client.exec_command(cmd)
            data = o.read()
            if data:
                return task['success'](data)
            else:
                return None

    def worker():
        while True:
            task = guess.get()
            new_info = threading.local()
            new_info.res = _get_info(task)
            if new_info.res:
                info.append(new_info.res)
            guess.task_done()

    for x in range(10):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    guess.join()

    if len(info) == 1:
        return info[0]
    else:
        return []


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
                re_port = re.search(
                    r'(?<=Connected Interface         :).*',
                    info)
                if re_port:
                    re_port = re_port.group()
                else:
                    re_port = "Unknown"
                connections.append({
                    'WWPN': wwpn,
                    'SW_IP': re.search('(?<=\()\d+(\.\d+){3}', info).group(),
                    'Port': re_port,
                    'VSAN': re.search(r'(?<=VSAN:)\d+', info).group(),
                    'SW_USR': switch.username,
                    'SW_PSW': switch.password,
                    'SW_VDR': switch.vendor,
                })
    elif switch.vendor == 'brocade':
        cmd = "nodefind "
        for wwpn in wwpns:
            (i, o, e) = sshc.exec_command(cmd + wwpn)
            info = o.read().decode('utf-8')
            if "No device found" not in info:
                temp = {
                    'WWPN': wwpn,
                    'Port': re.search(r'(?<=Port Index: )\w+', info).group(),
                    'SW_USR': switch.username,
                    'SW_PSW': switch.password,
                    'SW_VDR': switch.vendor,
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
