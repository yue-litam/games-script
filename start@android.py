# coding: utf-8

import sys

from common.device.c_android import AndroidDevice
from common.eventloop import EventLoop
from runtime import Config, Variables
from arknights.load_scenes import load_scenes as arknights_scenes
from azurelane.load_scenes import load_scenes as azurelane_scenes


def load_scenes(config, variables):
    if config.game_name == 'arknights':
        prefix = config.game_name + '/assets/640x1136/feature/'
        return arknights_scenes(prefix, config, variables)
    elif config.game_name == 'azurelane':
        prefix = config.game_name + '/assets/640x1136/feature/'
        return azurelane_scenes(prefix, config, variables)
    else:
        print('请指定游戏名称')
        exit(0)


if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)

if __name__ == '__main__':
    # 1. init config
    cfg = Config()
    var = Variables()

    # 2. init scenes
    scenes = load_scenes(cfg, var)

    # 3. init device
    device = AndroidDevice(log_level=cfg.log_level, address='127.0.0.1:7555')
    var.device_screen_width = device.screen_x
    var.device_screen_height = device.screen_y

    # 4. init event loop and start.
    worker = EventLoop(scenes, device, variables=var, log_level=cfg.log_level)
    worker.start(3)
