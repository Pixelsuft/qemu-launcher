import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.sets import Ui_MainWindow
import config
import builtins


vm = builtins.vm_to_setup
vm_path = vm + '.vm'
conf = {}


names = {
    'fd': 'Floppy Disk',
    'hd': 'Hard Disk',
    'cd': 'CDROM'
}
filters = {
    'fd': '*.img;*.flp;*vfd;*.ima',
    'hd': '*.img;*.vhd;*.raw;*.qcow;*.qcow2',
    'cd': '*.iso;*.cdrom'
}
last_path = ''
added_items = []


def s(param, value):
    conf[param] = value


def dialog(filetype, obj):
    global last_path
    if not last_path:
        last_path = os.getcwd()
    filepath = QtWidgets.QFileDialog.getOpenFileName(
        MainWindow,
        f'Select ' +
        names[filetype],
        last_path,
        filters[filetype])[0]
    obj.setText(filepath)


def add_device():
    cur = ui.devices.currentItem().text()
    if cur in added_items:
        return
    ui.usingDevice.addItem(cur)
    added_items.append(cur)


def remove_device():
    cur = ui.devices.currentItem().text()
    ui.usingDevice.takeItem(ui.devices.currentRow())
    added_items.remove(cur)


def setup_events():
    ui.cancelButton.clicked.connect(lambda: sys.exit(0))
    ui.okButton.clicked.connect(lambda: sys.exit(on_exit(0)))
    ui.fdaButton.clicked.connect(lambda: dialog('fd', ui.fdaEdit))
    ui.fdbButton.clicked.connect(lambda: dialog('fd', ui.fdbEdit))
    ui.hdaButton.clicked.connect(lambda: dialog('hd', ui.hdaEdit))
    ui.hdbButton.clicked.connect(lambda: dialog('hd', ui.hdbEdit))
    ui.hdcButton.clicked.connect(lambda: dialog('hd', ui.hdcEdit))
    ui.hddButton.clicked.connect(lambda: dialog('hd', ui.hddEdit))
    ui.cdButton.clicked.connect(lambda: dialog('cd', ui.cdEdit))
    ui.addDevice.clicked.connect(add_device)
    ui.removeDevice.clicked.connect(remove_device)


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
    ui.cs4231a.setChecked(c['cs4231a'])
    ui.hda.setChecked(c['ihda'])
    ui.adlib.setChecked(c['adlib'])
    ui.sb16.setChecked(c['sb16'])
    ui.pcspk.setChecked(c['pcspk'])
    ui.es1370.setChecked(c['es1370'])
    ui.gus.setChecked(c['gus'])
    ui.fdaEdit.setText(c['fda'])
    ui.fdbEdit.setText(c['fdb'])
    ui.hdaEdit.setText(c['hda'])
    ui.hdbEdit.setText(c['hdb'])
    ui.hdcEdit.setText(c['hdc'])
    ui.hddEdit.setText(c['hdd'])
    ui.cdEdit.setText(c['cd'])
    ui.usbEdit.setChecked(c['usb'])
    for i in c['devices']:
        ui.usingDevice.addItem(i)
        added_items.append(i)
    ui.otherargsEdit.setText(c['otherargs'])
    ui.mytoolsEdit.setChecked(c['mytools'])
    ui.ctrlgrabEdit.setChecked(c['ctrlgrab'])
    ui.altgrabEdit.setChecked(c['altgrab'])
    ui.sudoEdit.setChecked(c['sudo'])
    ui.nodefaultEdit.setChecked(c['nodefaults'])
    ui.orderEdit.setCurrentText(c['order'])


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
    s('cs4231a', ui.cs4231a.isChecked())
    s('ihda', ui.hda.isChecked())
    s('adlib', ui.adlib.isChecked())
    s('ac97', ui.ac97.isChecked())
    s('sb16', ui.sb16.isChecked())
    s('pcspk', ui.pcspk.isChecked())
    s('es1370', ui.es1370.isChecked())
    s('gus', ui.gus.isChecked())
    s('fda', ui.fdaEdit.text())
    s('fdb', ui.fdbEdit.text())
    s('hda', ui.hdaEdit.text())
    s('hdb', ui.hdbEdit.text())
    s('hdc', ui.hdcEdit.text())
    s('hdd', ui.hddEdit.text())
    s('cd', ui.cdEdit.text())
    s('usb', ui.usbEdit.isChecked())
    s('devices', added_items)
    s('otherargs', ui.otherargsEdit.text())
    s('mytools', ui.mytoolsEdit.isChecked())
    s('sudo', ui.sudoEdit.isChecked())
    s('ctrlgrab', ui.ctrlgrabEdit.isChecked())
    s('altgrab', ui.altgrabEdit.isChecked())
    s('nodefaults', ui.nodefaultEdit.isChecked())
    s('order', ui.orderEdit.currentText())


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
