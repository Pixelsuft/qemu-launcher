import sys
import builtins


argc = len(sys.argv)


if argc <= 2:
    import manage
else:
    if sys.argv[1] == '--run_vm':
        builtins.vm_to_run = sys.argv[2]
        import run_vm
    elif sys.argv[1] == '--setup_vm':
        builtins.vm_to_setup = sys.argv[2]
        import setup_vm
