import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.sets import Ui_MainWindow
import config
import builtins


vm = builtins.vm_to_setup
vm_path = vm + '.vm'
conf = {}


def s(param, value):
    conf[param] = value


def setup_events():
    ui.cancelButton.clicked.connect(lambda: sys.exit(0))
    ui.okButton.clicked.connect(lambda: sys.exit(on_exit(0)))


def process_config(c):
    ui.archEdit.setCurrentIndex(int(c['arch'] == '64-bit'))
    ui.cpu_edit.setCurrentText(conf['cpu'])


def apply_config():
    s('arch', ui.archEdit.currentText())
    s('cpu', ui.cpu_edit.currentText())


def on_init():
    global conf
    MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
    conf = config.read_config(vm_path)
    if conf:
        process_config(conf)
    setup_events()


def on_exit(to_exit_code):
    apply_config()
    config.write_config(vm_path, conf)
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
