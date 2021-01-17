# coding: utf-8
import atexit
import sys

from common.device.c_android import AndroidDevice
from common.device.c_ios import IOSDevice
from common.eventloop import EventLoop
from common.logutil import logger
from common.runtime import Config, Context
from games.arknights.load_scenes import load_scenes as arknights_scenes
from games.azurelane.load_scenes import load_scenes as azurelane_scenes
from games.girlsfrontline.load_scenes import load_scenes as gf_scenes


def load_scenes(config, context):
    prefix = './games/' + config.game_name + '/assets/'
    if config.game_name == 'arknights':
        return arknights_scenes(prefix, config, context)
    elif config.game_name == 'azurelane':
        return azurelane_scenes(prefix, config, context)
    elif config.game_name == 'girlsfrontline':
        return gf_scenes(prefix, config, context)
    else:
        logger.error('请指定游戏名称')
        exit(1)


# see reference https://learnku.com/docs/pymotw/atexit-program-shutdown-callbacks/3458
@atexit.register
def goodbye():
    logger.info("You are now leaving the Python sector. Goodbye~ \n\n\n")


cfg = None
ctx = None

if sys.version_info.major != 3:
    logger.error('请使用python3.x版本')
    exit(1)

if __name__ == '__main__':
    try:
        # 1. init config
        cfg = Config()
        ctx = Context()
        logger.info(cfg)

        # 2. init scenes
        scenes = load_scenes(cfg, ctx)

        # 3. init device
        if cfg.device_type == 'ios':
            device = IOSDevice(cfg=cfg)
        elif cfg.device_type == 'android':
            device = AndroidDevice(cfg=cfg)
        else:
            raise EnvironmentError("未知的设备类型")
        ctx.screen_width = device.screen_x
        ctx.screen_height = device.screen_y

        # 4. init event loop and start.
        worker = EventLoop(scenes, device, ctx)
        worker.start()
    except KeyboardInterrupt:
        print()
        logger.info('Ctrl+C 被按下, 程序即将退出.')
        exit(0)
    except Exception as unknown:
        print()
        logger.error("Unexcepted/Unkonwn Exception occurred")
        logger.exception(unknown)
        exit(1)
