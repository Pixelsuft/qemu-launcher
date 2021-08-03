import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.runner import Ui_MainWindow
import config
from threading import Thread
import builtins
from pynput import keyboard
import time
import signal


vm = builtins.vm_to_run
is_in_boot = False


def process(process_type):
    MainWindow.hide()
    builtins.qemu_conf = {
        'sets': config.read_config(vm + '.vm'),
        'pid': os.getpid(),
        'vm_name': vm,
        'boot_from': process_type
    }
    import qemu_parser


def on_press(key):
    global is_in_boot
    if is_in_boot:
        need = str(key)
        if need == "'1'":
            process('fd')
        elif need == "'2'":
            process('hd')
        elif need == "'3'":
            process('cd')
        return False
    else:
        if key == keyboard.Key.f2:
            is_in_boot = True
            ui.label.setPixmap(QtGui.QPixmap("images/win10_menu.png"))


listener = keyboard.Listener(on_press=on_press)


def setup_events():
    listener.start()


def sleep_thread():
    time.sleep(3)
    if not is_in_boot:
        process('default')


def on_init():
    MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
    setup_events()
    Thread(target=sleep_thread).start()


def on_exit(to_exit_code):
    listener.stop()
    os.kill(os.getpid(), signal.SIGTERM)
    if not to_exit_code == 0:
        print('Error exit!', to_exit_code)
    return to_exit_code


app = QtWidgets.QApplication([__file__])
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
on_init()
MainWindow.show()
sys.exit(on_exit(app.exec_()))
