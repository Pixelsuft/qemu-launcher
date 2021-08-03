import builtins
from threading import Thread
import os
import signal
import sys


sets = builtins.qemu_conf['sets']
pid = builtins.qemu_conf['pid']
vm_name = builtins.qemu_conf['vm_name']
boot_from = builtins.qemu_conf['boot_from']


args = []
cmd = ''


def win_thread():
    if not sys.platform == 'win32' or not sets['mytools']:
        return
    print('continue')


def qemu_thread():
    os.system(cmd)
    os.kill(pid, signal.SIGTERM)


Thread(target=win_thread).start()
qemu_thread()
