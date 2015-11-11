import threading
import queue
import winrm
import json


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
        'script': '/scripts/get_info.py',
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
            # TODO add paramiko part here!
            pass
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

def get_connection_info(wwpn):
    # TODO find the connection info for the wwpn
    pass
