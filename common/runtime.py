import os
import sys
from configparser import ConfigParser
from shutil import copyfile


class Config:
    # ---- global config ----
    game_name = ""
    repeat_count_max = -1
    device_type = ""
    screenshot_to_disk = False
    screenshot_to_disk_file_name = None

    # ---- azurelane config ----
    battle_no = ""
    default_swipe_direction = 0
    team_switch = False
    team_switch_threshold = 5

    # ---- arknights config ----
    use_pharmacy_max = 0
    use_stone_max = 0

    # ---- girlsfrontline ----
    max_like_dormitory = 0

    def __init__(self):
        # 从配置文件读取配置
        cfg = self.__load_configuration_file()
        self.device_type = cfg.get('global', 'device_type')
        self.game_name = cfg.get('global', 'game_name')
        self.repeat_count_max = cfg.getint('global', 'repeat_count_max')
        self.server_chan_enable = cfg.getboolean('global', 'server_chan_enable')
        self.server_chan_secret = cfg.get('global', 'server_chan_secret')
        self.screenshot_to_disk = cfg.getboolean('global', 'screenshot_to_disk')
        self.screenshot_to_disk_file_name = cfg.get('global', 'screenshot_to_disk_file_name')

        self.use_stone_max = cfg.getint('arknights', 'use_stone_max')
        self.use_pharmacy_max = cfg.getint('arknights', 'use_pharmacy_max')

        self.battle_no = cfg.get('azurelane', 'battle_no')
        self.default_swipe_direction = cfg.getint('azurelane', 'default_swipe_direction')
        self.team_switch = cfg.getboolean('azurelane', 'team_switch')
        self.team_switch_threshold = cfg.getint('azurelane', 'team_switch_threshold')

        self.max_like_dormitory = cfg.getint('girlsfrontline', 'max_like_dormitory')
        if self.game_name == 'arknights':
            self.battle_no = '(无)'

        # 如果有命令行参数，更新覆盖配置
        self.__override_from_command_line()

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
        if args_count == 1:
            return
        elif args_count > 1 and args[1] == '-h' or args[1] == '--help':
            print('  -h,  --help         查看所有支持的参数')
            print('  -g,  --game         游戏名称，枚举:azurelane, arknights, girlsfrontline')
            print('  -r,  --repeat       复读次数')
            print('  -s,  --save         屏幕截图是否保存到本地磁盘')
            print('  -sf, --save-file    屏幕截图保存到本地磁盘的路径')
            print('  -azlb               碧蓝航线(azurelane)复读的关卡名称,如: 3_1, 7_3')
            print('  -arkp               明日方舟(arknights)药剂使用数量')
            print('  -arks               明日方舟(arknights)源石使用数量')
            exit(0)
        else:
            if (args_count - 1) % 2 != 0:
                raise AttributeError('请检查输入的命令行参数')
            pairs = (args_count - 1) // 2
            offset = 1
            for i in range(pairs):
                name_index = i * 2 + offset
                valv_index = name_index + 1
                if args[name_index] == '-g' or args[name_index] == '--game':
                    self.game_name = args[valv_index]
                elif args[name_index] == '-r' or args[name_index] == '--repeat':
                    self.repeat_count_max = int(args[valv_index])
                elif args[name_index] == '-s' or args[name_index] == '--save':
                    self.screenshot_to_disk = bool(args[valv_index])
                elif args[name_index] == '-sf' or args[name_index] == '--save-file':
                    self.screenshot_to_disk_file_name = args[valv_index]
                elif args[name_index] == '-azlb':
                    self.battle_no = args[valv_index]
                elif args[name_index] == '-arkp':
                    self.use_pharmacy_max = int(args[valv_index])
                elif args[name_index] == '-arks':
                    self.use_stone_max = int(args[valv_index])

    def __str__(self):
        _str = '\n'
        _str += '屏幕截图位置：{0}\n'.format(self.screenshot_to_disk_file_name if self.screenshot_to_disk else '(None)')
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
    game = ""
    screen_width = 1136
    screen_height = 640

    repeated_count = 0  # 复读次数
    flag_start_printed = False

    # ---- azurelane ----
    search_enemy = False  # 进入索敌界面
    team_switched = False
    swipe_mode = 0  # 索敌为空时，移动地图方向，0=向上滑动，1=向右滑动，2=向下滑动，3=向左滑动
    round_count = 0

    # ---- arknights ----
    pharmacy_used = 0  # 已使用的药剂数量，初识为0
    stone_used = 0  # 已使用的源石数量，初识为0

    # ---- girlsfrontline ----
    like_friend_dormitory_count = 0
