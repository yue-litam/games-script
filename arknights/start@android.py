# coding: utf-8

from configparser import ConfigParser

from android import AndroidEventLoop
from loadscenes import *
from runtime import Runtime

sys.path.insert(1, '../common')

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)


if __name__ == '__main__':
    cfg = ConfigParser()
    runtime = Runtime()
    try:
        cfg.read('config.ini')
        runtime.use_stone_auto = cfg.getboolean('intellect', 'use_stone')
        runtime.use_stone_max = cfg.getint('intellect', 'use_stone_max')
        runtime.use_pharmacy_auto = cfg.getboolean('intellect', 'use_pharmacy')
        runtime.use_pharmacy_max = cfg.getint('intellect', 'use_pharmacy_max')
        print('理智不足时')
        print('\t自动使用药剂:{0}, 最多使用数量:{1}'.format(runtime.use_pharmacy_auto, runtime.use_pharmacy_max))
        print('\t自动使用石头:{0}, 最多使用数量:{1}'.format(runtime.use_stone_auto, runtime.use_stone_max))
        print('')
    except Exception as ex:
        print(ex)

    prefix = 'assets/640x1136/feature/'
    # prefix = 'assets/810x1440/feature/'
    eventLoop = AndroidEventLoop()
    eventLoop.scenes = [
        prts_disable_detection(eventLoop, prefix),  # 战斗关卡确认出击
        account_upgrade_detection(eventLoop, prefix),  # 战斗结束后账号等级提升
        level_info_detection(eventLoop, prefix),  # 战斗关卡确认出击
        level_team_detection(eventLoop, prefix, runtime),  # 战斗前队伍预览
        level_finish_detection(eventLoop, prefix),  # 战斗结束后账号等级提升
        prts_running_scene(eventLoop, prefix),  # 副本还在进行中
        exchange_intellect_by_pharmacy(eventLoop, prefix, runtime),  # 理智不足时有可使用的药剂
        exchange_intellect_by_stone(eventLoop, prefix, runtime),  # 理智不足时有可使用的石头
    ]
    eventLoop.start()
