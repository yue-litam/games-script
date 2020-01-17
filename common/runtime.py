import os
import sys
from configparser import ConfigParser
from shutil import copyfile

from common.logutil import logger


class Config:
    # ---- global config ----
    game_name = ''
    repeat_count_max = -1
    device_type = ''
    device_dpi = 1

    # ---- azurelane config ----
    battle_no = ''
    default_swipe_direction = 0  # 移动地图进行索敌时的首次移动方向

    # ---- arknights config ----
    use_pharmacy_max = 0
    use_stone_max = 0

    def __init__(self):
        try:
            # 从配置文件读取配置
            cfg = self.__load_configuration_file()
            self.device_type = cfg.get('global', 'device_type')
            self.device_dpi = cfg.getint('global', 'device_dpi')
            self.game_name = cfg.get('global', 'game_name')
            self.repeat_count_max = cfg.getint('global', 'repeat_count_max')
            self.use_stone_max = cfg.getint('arknights', 'use_stone_max')
            self.use_pharmacy_max = cfg.getint('arknights', 'use_pharmacy_max')
            self.battle_no = cfg.get('azurelane', 'battle_no')
            self.default_swipe_direction = cfg.getint('azurelane', 'default_swipe_direction')

            # 如果有命令行参数，更新覆盖配置
            self.__override_from_command_line()

            logger.info(self)
        except Exception as ex:
            logger.error(ex)

    @staticmethod
    def __load_configuration_file():
        cfg = ConfigParser()
        config_file_name = 'conf/config.ini'
        if not os.path.exists(config_file_name):
            # see reference:https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
            copyfile('conf/default-config.ini', config_file_name)
        cfg.read(config_file_name, encoding="utf-8")
        return cfg

    def __override_from_command_line(self):
        args = sys.argv
        args_count = len(args)  # always >=1, first is main entry file path.
        if args_count > 1:
            self.game_name = args[1]
        if self.game_name == 'azurelane' and args_count > 2:
            self.battle_no = args[2]

    def __str__(self):
        _str = '\n'
        _str += '当前复读游戏：{0}\n'.format(self.game_name)
        _str += '最多复读次数: {0}\n'.format(self.repeat_count_max)
        if self.game_name == 'arknights':
            _str += ' - 理智不足时\n'
            _str += '  - 自动使用药剂:{0}\n'.format(self.use_pharmacy_max)
            _str += '  - 自动使用石头:{0}\n'.format(self.use_stone_max)
        elif self.game_name == 'azurelane':
            _str += ' - 关卡: {}\n'.format(self.battle_no)
        _str += '\n'
        return _str


class Context:
    # ---- global ----
    game = ''
    screen_width = 1136
    screen_height = 640

    repeated_count = 0  # 复读次数
    flag_start_printed = False

    # ---- azurelane ----
    search_enemy = False  # 进入索敌界面
    swipe_mode = 0  # 索敌为空时，移动地图方向，0=向上滑动，1=向右滑动，2=向下滑动，3=向左滑动
    round_count = 0

    # ---- arknights ----
    pharmacy_used = 0  # 已使用的药剂数量，初识为0
    stone_used = 0  # 已使用的源石数量，初识为0
