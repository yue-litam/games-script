# coding: utf-8

import sys
from common.device.c_ios import IOSDevice
from common.eventloop import EventLoop
from runtime import Config, Variables
from arknights.load_scenes import load_scenes as arknights_scenes
from azurelane.load_scenes import load_scenes as azurelane_scenes
from logutil import logger


def load_scenes(config, variables):
    prefix = config.game_name + '/assets/scenes_feature/'
    if config.game_name == 'arknights':
        return arknights_scenes(prefix, config, variables)
    elif config.game_name == 'azurelane':
        return azurelane_scenes(prefix, config, variables)
    else:
        logger.error('请指定游戏名称')
        exit(0)


if sys.version_info.major != 3:
    logger.error('请使用python3.x版本')
    exit(1)

if __name__ == '__main__':
    # 1. init config
    cfg = Config()
    var = Variables()

    # 2. init scenes
    scenes = load_scenes(cfg, var)

    # 3. init device
    dpi = 2  # iphone SE 的屏幕DPI为2，使用wda发送触摸指令时坐标(x,y)需要除以相应的dpi
    device = IOSDevice(dpi, address='http://127.0.0.1:8100')

    # 4. init event loop and start.
    worker = EventLoop(scenes, device, variables=var)
    worker.start()
