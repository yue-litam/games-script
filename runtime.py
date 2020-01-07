import os
import sys
from configparser import ConfigParser
from shutil import copyfile
from logutil import logger


class Config:
    # ---- global config ----
    game_name = ''
    repeat_count_max = -1

    # ---- azurelane config ----
    battle_no = ''

    # ---- arknights config ----
    use_pharmacy_max = 0
    use_stone_max = 0

    def __init__(self):
        args = sys.argv
        args_count = len(args)  # always >=1, first is main entry file path.
        cfg = ConfigParser()
        config_file_name = 'config.ini'
        try:
            # see reference:https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
            if not os.path.exists(config_file_name):
                copyfile('default-config.ini', config_file_name)
            cfg.read(config_file_name, encoding="utf-8")

            if args_count > 1:
                self.game_name = args[1]
            else:
                self.game_name = cfg.get('global', 'game_name')
            self.repeat_count_max = cfg.getint('global', 'repeat_count_max')
            logger.info('游戏最多复读次数: {0}'.format(self.repeat_count_max))

            if self.game_name == 'arknights':
                self.use_stone_max = cfg.getint(self.game_name, 'use_stone_max')
                self.use_pharmacy_max = cfg.getint(self.game_name, 'use_pharmacy_max')
                logger.info('当前复读游戏：明日方舟')
                logger.info(' - 理智不足时')
                logger.info('  - 自动使用药剂:{0}'.format(self.use_pharmacy_max))
                logger.info('  - 自动使用石头:{0}'.format(self.use_stone_max))
            elif self.game_name == 'azurelane':
                if args_count > 2:
                    self.battle_no = args[2]
                else:
                    self.battle_no = cfg.get(self.game_name, 'battle_no')
                logger.info('当前复读游戏：碧蓝航线')
                logger.info(' - 关卡: {}'.format(self.battle_no))
            logger.info('')
        except Exception as ex:
            logger.error(ex)


class Variables:
    # ---- global ----
    game = ''
    device_screen_width = 1136
    device_screen_height = 640

    repeated_count = 0  # 复读次数
    flag_start_printed = False

    # ---- azurelane ----
    search_enemy = False  # 进入索敌界面
    swipe_mode = 2  # 索敌为空时，移动地图方向，0=向上滑动，1=向右滑动，2=向下滑动，3=向左滑动
    round_count = 0

    # ---- arknights ----
    pharmacy_used = 0  # 已使用的药剂数量，初识为0
    stone_used = 0  # 已使用的源石数量，初识为0
