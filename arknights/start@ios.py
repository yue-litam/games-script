# coding: utf-8

import sys

from ios import IOSEventLoop

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)

if __name__ == '__main__':
    prefix = 'assets/640x1136/feature/'
    dpi = 2  # iphone SE 的屏幕DPI为2，使用wda发送触摸指令时坐标(x,y)需要除以相应的dpi，安卓就没这毛病
    IOSEventLoop(prefix, dpi).start()
