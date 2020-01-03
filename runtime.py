from configparser import ConfigParser
import sys


class Config:
    # ---- global config ----
    game_name = ''
    repeat_count_max = -1
    log_level = 'info'

    # ---- azurelane config ----
    battle_no = ''

    # ---- arknights config ----
    use_pharmacy_max = 0
    use_stone_max = 0

    def __init__(self):
        args = sys.argv
        args_count = len(args)  # always >=1, first is main entry file path.
        cfg = ConfigParser()
        try:
            cfg.read('config.ini', encoding="utf-8")
            if args_count > 1:
                self.game_name = args[1]
            else:
                self.game_name = cfg.get('global', 'game_name')
            self.log_level = cfg.get('global', 'log_level')
            self.repeat_count_max = cfg.getint('global', 'repeat_count_max')
            print('游戏最多复读次数: {0}'.format(self.repeat_count_max))

            if self.game_name == 'arknights':
                self.use_stone_max = cfg.getint(self.game_name, 'use_stone_max')
                self.use_pharmacy_max = cfg.getint(self.game_name, 'use_pharmacy_max')
                print('当前复读游戏：明日方舟')
                print(' - 理智不足时')
                print('  - 自动使用药剂:{0}'.format(self.use_pharmacy_max))
                print('  - 自动使用石头:{0}'.format(self.use_stone_max))
            elif self.game_name == 'azurelane':
                if args_count > 2:
                    self.battle_no = args[2]
                else:
                    self.battle_no = cfg.get(self.game_name, 'battle_no')
                print('当前复读游戏：碧蓝航线')
                print(' - 关卡: {}'.format(self.battle_no))
            print('')
        except Exception as ex:
            print(ex)


class Variables:
    # ---- global ----
    game = ''
    device_screen_width = 1136
    device_screen_height = 640

    repeated_count = 0  # 复读次数
    flag_start_printed = False

    # ---- azurelane ----
    search_enemy = False  # 进入索敌界面
    swipe_mode = 0  # 索敌为空时，移动地图方向，0=向上滑动，1=向右滑动，2=向下滑动，3=向左滑动
    round_count = 0

    # ---- arknights ----
    pharmacy_used = 0  # 已使用的药剂数量，初识为0
    stone_used = 0  # 已使用的源石数量，初识为0
