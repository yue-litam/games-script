# coding: utf-8

import sys
from common.device.c_ios import IOSDevice
from common.eventloop import EventLoop
from runtime import Runtime
from arknights.load_scenes import load_scenes as arknights_scenes
from azurelane.load_scenes import load_scenes as azurelane_scenes

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)

if __name__ == '__main__':

    # 1. init runtime config
    rt = Runtime()

    # 2. init scenes
    prefix = rt.game + '/assets/640x1136/feature/'
    scenes = None
    if rt.game == 'arknights':
        scenes = arknights_scenes(prefix, runtime=rt)
    elif rt.game == 'azurelane':
        scenes = azurelane_scenes(prefix, runtime=rt)
    else:
        print('请指定游戏名称')
        exit(0)

    # 3. init device
    dpi = 2  # iphone SE 的屏幕DPI为2，使用wda发送触摸指令时坐标(x,y)需要除以相应的dpi
    device = IOSDevice(dpi, runtime=rt, address='http://127.0.0.1:8100')

    # 4. init event loop and start.
    worker = EventLoop(scenes, device, rt)
    worker.start()
