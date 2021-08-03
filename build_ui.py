import os
import sys
from fasttools import read_file, write_file, file_exists


if file_exists('ui/manager.py'):
    os.remove('ui/manager.py')

if os.system('pyuic5 ui/manager.ui -o ui/manager.py -x'):
    print('build error')
    sys.exit(1)


if file_exists('ui/sets.py'):
    os.remove('ui/sets.py')

if os.system('pyuic5 ui/sets.ui -o ui/sets.py -x'):
    print('build error')
    sys.exit(1)


if file_exists('ui/runner.py'):
    os.remove('ui/runner.py')

if os.system('pyuic5 ui/runner.ui -o ui/runner.py -x'):
    print('build error')
    sys.exit(1)


write_file('ui/manager.py', read_file('ui/manager.py').replace('ui\\\\../', '').replace('ui/../', ''))
write_file('ui/sets.py', read_file('ui/sets.py').replace('ui\\\\../', '').replace('ui/../', ''))
write_file('ui/runner.py', read_file('ui/runner.py').replace('ui\\\\../', '').replace('ui/../', ''))
print('Ok!')
