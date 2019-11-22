from configparser import ConfigParser


class Runtime:
    # ---- global config ----
    round_count = 0
    log_level = 'info'
    game = ''
    # ---- global config ----

    # ---- azurelane config ----
    battle_no = ''
    # ---- azurelane config ----

    # ---- arknights config ----
    use_pharmacy_auto = False
    use_pharmacy_max = 0
    used_pharmacy_count = 0

    use_stone_auto = False
    use_stone_max = 0
    used_stone_count = 0
    # ---- arknights config ----

    def __init__(self):
        cfg = ConfigParser()
        try:
            cfg.read('config.ini')
            self.log_level = cfg.get('global', 'log_level')
            self.game = cfg.get('global', 'game_name')

            self.use_stone_auto = cfg.getboolean('arknights', 'intellect_use_stone')
            self.use_stone_max = cfg.getint('arknights', 'intellect_use_stone_max')
            self.use_pharmacy_auto = cfg.getboolean('arknights', 'intellect_use_pharmacy')
            self.use_pharmacy_max = cfg.getint('arknights', 'intellect_use_pharmacy_max')

            print('明日方舟')
            print('  - 理智不足时')
            print('    - 自动使用药剂:{0}, 最多使用数量:{1}'.format(self.use_pharmacy_auto, self.use_pharmacy_max))
            print('    - 自动使用石头:{0}, 最多使用数量:{1}'.format(self.use_stone_auto, self.use_stone_max))

            self.battle_no = cfg.get('azurelane', 'battle_no')
            print('碧蓝航线')
            print('  - 复读关卡: {}'.format(self.battle_no))
            print('')
        except Exception as ex:
            print(ex)
