# coding: utf-8

import sys

from common.device.c_android import AndroidDevice
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
    elif rt.game == 'arknights':
        scenes = azurelane_scenes(prefix, runtime=rt)
    else:
        print('请指定游戏名称')
        exit(0)

    # 3. init device
    device = AndroidDevice(runtime=rt, address='http://127.0.0.1:7555')

    # 4. init event loop and start.
    worker = EventLoop(scenes, device)
    worker.start()
