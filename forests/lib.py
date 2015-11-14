import threading
import queue
import winrm
import json
import paramiko
from django.conf import settings
import os


def get_server_info(server):
    info = []
    guess = queue.Queue()
    # call ansible API to deploy the scripts in the future but now we
    # assumed that the scripts were already deployed.
    # maybe we can use a share folder to hold all the scripts and then mount
    # the folder ready only to the hosts.
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
