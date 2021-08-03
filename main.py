import sys
import builtins
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget


argc = len(sys.argv)


try:
    if argc <= 2:
        import manage
    else:
        if sys.argv[1] == '--run_vm':
            builtins.vm_to_run = sys.argv[2]
            import run_vm
        elif sys.argv[1] == '--setup_vm':
            builtins.vm_to_setup = sys.argv[2]
            import setup_vm
except Exception as e:
    msg = QMessageBox.critical(QWidget(), 'Error', f'App crashed with error:\n{e}')
    sys.exit(1)

