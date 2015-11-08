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
        'script': 'C:\scripts\Get-HBAWin.ps1'
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
                r = s.run_ps(task['script'])
            except:
                # TODO put the exception detail into log
                return None
            if r.status_code == 0:
                json_str = r.std_out.rstrip("\\r\\n'").lstrip("b'")
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
