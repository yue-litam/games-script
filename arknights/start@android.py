# coding: utf-8

import sys

from android import AndroidEventLoop

sys.path.insert(1, '../common')

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)

if __name__ == '__main__':
    prefix = 'assets/640x1136/feature/'
    AndroidEventLoop(prefix).start()
