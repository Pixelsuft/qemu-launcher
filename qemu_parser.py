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
if s['mtkvm']:
    args.append('-accel')
    args.append('kvm,thread=multi')
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

args.append('-no-reboot')
args.append('-name')
args.append(vm_name)
print(args)


def win_thread():
    if not sys.platform == 'win32' or not s['mytools'] or (not s['sdl'] and not s['display'] == 'SDL'):
        return
    import win32api
    import win32con
    import win32gui
    print('continue')


def qemu_thread():
    os.system(cmd)
    os.kill(pid, signal.SIGTERM)


Thread(target=win_thread).start()
qemu_thread()
