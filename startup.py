import os
import subprocess


def start():
    if ((os.environ.get('MULTI_SERVER') or '0') == '1' and (os.environ.get('ASSISTANT') or '0') == '1')\
        or (os.environ.get('MULTI_SERVER') or '0') == '0':
        migrate_path = os.path.join(os.curdir, 'data/migrations')
        if not os.path.exists(migrate_path):
            argv = ['python', 'manage.py', 'db', 'init']
            proc = subprocess.Popen(argv)
            if proc.wait() != 0:
                return 0
        argv = ['python', 'manage.py', 'db', 'migrate']
        proc = subprocess.Popen(argv)
        if proc.wait() != 0:
            return 0
        argv = ['python', 'manage.py', 'db', 'upgrade']
        proc = subprocess.Popen(argv)
        if proc.wait() != 0:
            return 0
    argv = [
        'gunicorn',
        '-c',
        'gunicorn.conf',
        'manage:app',
        '--preload'
    ]
    # argv = [
    #     'python',
    #     'run.py',
    # ]
    proc = subprocess.Popen(argv)
    if proc.wait() != 0:
        return 0
    return 1


if __name__ == '__main__':
    start()
