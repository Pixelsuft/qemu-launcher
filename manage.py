import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.manager import Ui_MainWindow
import config
import subprocess
from threading import Thread


all_machines = []
current_machine = ''


def create_vm():
    text, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Create VM', 'Enter name of the Virtual Machine:')
    if ok and text not in all_machines:
        all_machines.append(text)
        ui.listVM.addItem(text)


def delete_vm():
    global current_machine
    index = all_machines.index(current_machine)
    all_machines.remove(current_machine)
    ui.listVM.takeItem(index)
    if all_machines:
        current_machine = ui.listVM.currentItem().text()
    else:
        ui.deleteVM.setEnabled(False)
        ui.loadVM.setEnabled(False)
        ui.configureVM.setEnabled(False)
        current_machine = ''


def change_vm(e):
    global current_machine
    if not all_machines:
        return
    current_machine = e.text()
    ui.deleteVM.setEnabled(True)
    ui.loadVM.setEnabled(True)
    ui.configureVM.setEnabled(True)


def run_vm():
    args = [sys.executable, 'main.py', '--run_vm', current_machine]
    Thread(target=lambda: subprocess.call(args)).start()


def setup_vm():
    args = [sys.executable, 'main.py', '--setup_vm', current_machine]
    Thread(target=lambda: subprocess.call(args)).start()


def setup_events():
    ui.quitApp.clicked.connect(lambda: sys.exit(on_exit(0)))
    ui.newVM.clicked.connect(create_vm)
    ui.deleteVM.clicked.connect(delete_vm)
    ui.loadVM.clicked.connect(run_vm)
    ui.configureVM.clicked.connect(setup_vm)
    ui.listVM.currentItemChanged.connect(change_vm)


def load_machines():
    machines = config.read_config('machines')
    if not machines or not machines['machines']:
        return
    for i in machines['machines']:
        all_machines.append(i)
        ui.listVM.addItem(i)


def on_init():
    MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
    load_machines()
    setup_events()


def on_exit(to_exit_code):
    machines_json = {
        'machines': all_machines
    }
    config.write_config('machines', machines_json)
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
