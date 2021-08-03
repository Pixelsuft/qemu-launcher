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
    ui.cpuEdit.setCurrentText(c['cpu'])
    ui.memoryEdit.setText(c['memory'])
    ui.biosEdit.setCurrentText(c['bios'])
    ui.coresEdit.setText(c['cores'])
    ui.hpetEdit.setChecked(c['hpet'])
    ui.acpiEdit.setChecked(c['acpi'])
    ui.kvmEdit.setChecked(c['kvm'])
    ui.mtkvmEdit.setChecked(c['mtkvm'])
    ui.whpxEdit.setChecked(c['whpx'])
    ui.tcgEdit.setChecked(c['tcg'])
    ui.mttcgEdit.setChecked(c['mttcg'])
    ui.haxmEdit.setChecked(c['haxm'])
    ui.speedEdit.setText(c['speed'])
    ui.videoEdit.setCurrentText(c['video'])
    ui.nographicEdit.setChecked(c['nographic'])
    ui.useconsoleEdit.setChecked(c['useconsole'])
    ui.monitorvcEdit.setChecked(c['monitorvc'])
    ui.monitorstdioEdit.setChecked(c['monitorstdio'])
    ui.serialvcEdit.setChecked(c['serialvc'])
    ui.serialstdioEdit.setChecked(c['serialstdio'])
    ui.displayEdit.setCurrentText(c['display'])
    ui.sdlEdit.setChecked(c['sdl'])
    ui.vncEdit.setText(c['vnc'])


def apply_config():
    s('arch', ui.archEdit.currentText())
    s('cpu', ui.cpuEdit.currentText())
    s('memory', ui.memoryEdit.text())
    s('bios', ui.biosEdit.currentText())
    s('cores', ui.coresEdit.text())
    s('hpet', ui.hpetEdit.isChecked())
    s('acpi', ui.acpiEdit.isChecked())
    s('kvm', ui.kvmEdit.isChecked())
    s('mtkvm', ui.mtkvmEdit.isChecked())
    s('whpx', ui.whpxEdit.isChecked())
    s('tcg', ui.tcgEdit.isChecked())
    s('mttcg', ui.mttcgEdit.isChecked())
    s('haxm', ui.haxmEdit.isChecked())
    s('speed', ui.speedEdit.text())
    s('video', ui.videoEdit.currentText())
    s('nographic', ui.nographicEdit.isChecked())
    s('useconsole', ui.useconsoleEdit.isChecked())
    s('monitorvc', ui.monitorvcEdit.isChecked())
    s('monitorstdio', ui.monitorstdioEdit.isChecked())
    s('serialvc', ui.serialvcEdit.isChecked())
    s('serialstdio', ui.serialstdioEdit.isChecked())
    s('display', ui.displayEdit.currentText())
    s('sdl', ui.sdlEdit.isChecked())
    s('vnc', ui.vncEdit.text())


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
