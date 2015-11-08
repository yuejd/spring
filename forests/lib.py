import threading
import queue


def get_server_info(server):
    info = []
    guess = queue.Queue()
    # call ansible API to deploy the scripts in the future but now we
    # assumed that the scripts were already deployed.
    # maybe we can use a share folder to hold all the scripts and then mount
    # the folder ready only to the hosts.
    guess.put({
        'type': 'windows',
        'script': 'c:\scripts\GetWinInfo.ps1',
        })
    guess.put({
        'type': 'linux',
        'script': '/scripts/get_info.py',
        })

    def _get_info(task):
        if task['type'] == 'windows':
            # run scripts via pywinrm
            pass
        elif task['type'] == 'linux':
            # run scripts via paramiko
            pass
        return None

    def worker():
        new_info = threading.local()
        task = guess.get()
        new_info = _get_info(task)
        if new_info:
            # convert it into JSON object
            info.append(new_info)
        guess.task_done

    for x in range(2):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    return info
