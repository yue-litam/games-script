# coding: utf-8

import sys

from ios import IOSEventLoop

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)

if __name__ == '__main__':
    prefix = 'assets/640x1136/feature/'
    IOSEventLoop(prefix).start()
