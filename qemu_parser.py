import builtins
from threading import Thread
import os
import signal
import sys


s = builtins.qemu_conf['sets']
pid = builtins.qemu_conf['pid']
vm_name = builtins.qemu_conf['vm_name']
boot_from = builtins.qemu_conf['boot_from']


args = []
cmd = ''
vid = {
    'Default VGA': 'std',
    'VMWARE SVGA 2': 'vmware',
    'Cirrus': 'cirrus',
    'VirtIO': 'virtio',
    'QXL': 'qxl',
    'RAM FB': 'ramfb',
    'None': 'none'
}

orders = {
    'CDROM/Hard Disk/Floppy': 'dca',
    'CDROM/Floppy/Hard Disk': 'dac',
    'Hard Disk/CDROM/Floppy': 'cda',
    'Hard Disk/Floppy/CDROM': 'cad',
    'Floppy/Hard Disk/CDROM': 'acd',
    'Floppy/CDROM/Hard Disk': 'adc',
}

if s['sudo']:
    args.append('sudo')
args.append('qemu-system-' + ('i386' if s['arch'] == '32-bit' else 'x86_64')
            + ('w' if (not s['useconsole'] and sys.platform == 'win32') else ''))
if s['nodefaults']:
    args.append('-nodefaults')
args.append('-cpu')
args.append(s['cpu'])
args.append('-m')
args.append(s["memory"])

if not s['bios'] == 'BIOS':
    bios = None
    if s['bios'] == 'EFI 32-bit (CIRRUS ONLY)':
        bios = 'efi32.bin'
    elif s['bios'] == 'EFI 64-bit (CIRRUS ONLY)':
        bios = 'efi64.bin'
    elif s['bios'] == 'EFI 32-bit (FIXED)':
        bios = 'efi32_fixed.bin'
    args.append('-bios')
    args.append(bios)

if not s['cores'] == '-1':
    args.append('-smp')
    args.append(s['cores'])

if not s['hpet']:
    args.append('-no-hpet')

if not s['acpi']:
    args.append('-no-acpi')

if s['kvm']:
    args.append('-accel')
    args.append('kvm,thread=single')
if s['tcg']:
    args.append('-accel')
    args.append('tcg,thread=single')
if s['mttcg']:
    args.append('-accel')
    args.append('tcg,thread=multi')
if s['whpx']:
    args.append('-accel')
    args.append('whpx')
if s['haxm']:
    args.append('-accel')
    args.append('hax')

if not s['speed'] == '-1':
    args.append('-rtc')
    args.append('base=localtime,clock=vm')
    args.append('-icount')
    args.append(f'shift={s["speed"]},align=off,sleep=off')

if s['nographic']:
    args.append('-nographic')

if s['video'] == 'ATI VGA':
    args.append('-device')
    args.append('ati-vga')
else:
    args.append('-vga')
    args.append(vid[s['video']])

if s['monitorvc']:
    args.append('-monitor')
    args.append('vc')
if s['monitorstdio']:
    args.append('-monitor')
    args.append('stdio')
if s['serialvc']:
    args.append('-serial')
    args.append('vc')
if s['serialstdio']:
    args.append('-serial')
    args.append('stdio')

args.append('-display')
if s['display'] == 'VNC':
    args.append(f'vnc={s["vnc"]}')
else:
    args.append(s['display'].lower())

if s['sdl']:
    args.append('-sdl')

if s['cs4231a']:
    args.append('-soundhw')
    args.append('cs4231a')
if s['ihda']:
    args.append('-soundhw')
    args.append('hda')
if s['adlib']:
    args.append('-soundhw')
    args.append('adlib')
if s['sb16']:
    args.append('-soundhw')
    args.append('sb16')
if s['pcspk']:
    args.append('-soundhw')
    args.append('pcspk')
if s['es1370']:
    args.append('-soundhw')
    args.append('es1370')
if s['gus']:
    args.append('-soundhw')
    args.append('gus')

if s['fda'].strip().replace(' ', ''):
    args.append('-fda')
    args.append(s['fda'])
if s['fdb'].strip().replace(' ', ''):
    args.append('-fdb')
    args.append(s['fdb'])
if s['hda'].strip().replace(' ', ''):
    args.append('-hda')
    args.append(s['hda'])
if s['hdb'].strip().replace(' ', ''):
    args.append('-hdb')
    args.append(s['hdb'])
if s['hdc'].strip().replace(' ', ''):
    args.append('-hdc')
    args.append(s['hdc'])
if s['hdd'].strip().replace(' ', ''):
    args.append('-hdd')
    args.append(s['hdd'])
if s['cd'].strip().replace(' ', ''):
    args.append('-cdrom')
    args.append(s['cd'])

args.append('-boot')
if boot_from == 'default':
    args.append(f'order={orders[s["order"]]},menu=off')
else:
    args.append(boot_from)

if s['usb']:
    args.append('-usb')

for i in s['devices']:
    args.append('-device')
    args.append(i)

if s['ctrlgrab']:
    args.append('-ctrl-grab')

if s['altgrab']:
    args.append('-alt-grab')

args.append('-no-reboot')
args.append('-name')
args.append(vm_name)


for i in args:
    cmd += ' '
    if ' ' in i:
        cmd += f'"{i}"'
    else:
        cmd += i

if s['otherargs']:
    cmd += ' '
    cmd += s['otherargs']

cmd = cmd.strip()


def win_thread():
    if not sys.platform == 'win32' or not s['mytools'] or (not s['sdl'] and not s['display'] == 'SDL'):
        return
    import win32api
    import win32ui
    import win32process
    import win32con
    import win32gui
    from pynput import keyboard
    import ctypes
    import ctypes.wintypes

    w = {
        'vga': None,
        'monitor': None,
        'serial': None
    }
    use_vga, use_monitor, use_serial = (not s['display'] == 'None' or s['sdl']),\
                                       (s['monitorvc'] or s['monitorstdio']), (s['serialvc'] or s['serialstdio'])

    if not use_vga and not use_monitor and not use_serial or not use_vga:
        return

    keys = keyboard.Controller()

    def get_current_show():
        if use_vga and not use_monitor and not use_serial or win32gui.IsWindowVisible(w['vga']):
            return 'vga'
        if win32gui.IsWindowVisible(w['monitor']):
            return 'monitor'
        if win32gui.IsWindowVisible(w['serial']):
            return 'serial'
        return 'vga'

    def send_to_monitor(command):
        cur = get_current_show()
        if not cur == 'monitor':
            win32gui.ShowWindow(w[cur], win32con.SW_HIDE)
            win32gui.ShowWindow(w['monitor'], win32con.SW_SHOW)
        win32gui.SetForegroundWindow(w['monitor'])
        keys.type(command)
        if not cur == 'monitor':
            win32gui.ShowWindow(w['monitor'], win32con.SW_HIDE)
            win32gui.ShowWindow(w[cur], win32con.SW_SHOW)
        win32gui.SetForegroundWindow(w[cur])

    is_ok = False

    while not is_ok:
        def enum_handler(hwnd, ctx):
            text = win32gui.GetWindowText(hwnd).strip()
            if 'QEMU' in text:
                if f'({vm_name}-0)' in text:
                    w['vga'] = hwnd
                elif f'({vm_name}-1)' in text:
                    w['monitor' if use_monitor else 'serial'] = hwnd
                elif f'({vm_name}-2)' in text and use_monitor:
                    w['serial'] = hwnd

        win32gui.EnumWindows(enum_handler, None)
        is_ok = w['vga'] and (w['monitor'] if use_monitor else True) and (w['serial'] if use_serial else True)

    vga_text = f'QEMU Launcher - {vm_name}'
    monitor_text = f'QEMU Launcher - {vm_name} - Monitor'
    serial_text = f'QEMU Launcher - {vm_name} - Serial'

    win32gui.InitCommonControls()

    old_h = win32gui.GetClientRect(w['vga'])[3]

    bar = win32gui.CreateMenu()
    file = win32gui.CreateMenu()

    def callback():
        print('xd')

    print(win32gui.GetWindowLong(w['vga'], 0))

    win32gui.AppendMenu(file, win32con.MF_STRING, 1000, "&Exit")
    win32gui.AppendMenu(bar, win32con.MF_POPUP, file, "&File")

    win32gui.SetMenu(w['vga'], bar)

    new_h = win32gui.GetClientRect(w['vga'])[3]

    left, top, width, height = win32gui.GetWindowRect(w['vga'])

    width -= left
    height -= top

    win32gui.MoveWindow(w['vga'], left, top, width, height - old_h + new_h, True)

    def test():
        print('blah')

    wnd = win32ui.CreateWindowFromHandle(w['vga'])

    while True:
        if not win32gui.GetWindowText(w['vga']) == vga_text:
            win32gui.SetWindowText(w['vga'], vga_text)
        if use_monitor:
            if not win32gui.GetWindowText(w['monitor']) == monitor_text:
                win32gui.SetWindowText(w['monitor'], monitor_text)
        if use_serial:
            if not win32gui.GetWindowText(w['serial']) == serial_text:
                win32gui.SetWindowText(w['serial'], serial_text)
        wnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)


def qemu_thread():
    os.system(cmd)
    os.kill(pid, signal.SIGTERM)


Thread(target=win_thread).start()
qemu_thread()
