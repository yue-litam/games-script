# import sys
# sys.path.insert(1, '../common')
from common.scene import Scene


def account_upgrade_detection(prefix=''):
    return Scene('account_upgrade_detection.png', prefix)


def prts_disable_detection(prefix=''):
    return Scene('prts_disable_detection.png', prefix)


def level_info_detection(prefix=''):
    scene = Scene('level_info_detection.png', prefix)
    scene.action_tap_offset_x = scene.action_image_w
    return scene


def prts_running_scene(prefix=''):
    def after_action():
        print('.', sep='', end='')

    return Scene('level_fighting_detection.png', prefix,
                 action_tap=False, after_action=after_action)


def level_team_detection(runtime, prefix=''):
    def before_action():
        if 0 < runtime.max_repeat_count <= runtime.round_count:
            print('\n\n预设的复读次数已完成')
            exit(0)
        runtime.round_count += 1
        if runtime.start_flag_printed:
            pass
        else:
            print('\n第 %03d 次副本' % runtime.round_count, sep='', end='')
            runtime.start_flag_printed = True

    return Scene('level_team_detection.png', prefix, before_action=before_action)


def level_finish_detection(runtime, prefix=''):
    def after_action():
        runtime.start_flag_printed = False
    return Scene('level_finish_detection.png', prefix, after_action=after_action)


def exchange_intellect_by_pharmacy(runtime, prefix=''):
    def before_action():
        if runtime.use_pharmacy_auto:
            if runtime.used_pharmacy_count >= runtime.use_pharmacy_max:
                print('\n\n已到达预设的可用理智上限, 脚本将退出')
                exit(0)
            else:
                runtime.used_pharmacy_count += 1
        else:
            print('理智不足，自动退出脚本')
            exit(0)

    return Scene('exchange_intellect_by_pharmacy.png', prefix,
                 before_action=before_action,
                 action_image="exchange_intellect_confirm.png")


def exchange_intellect_by_stone(runtime, prefix=''):
    if runtime is None:
        raise Exception('runtime config is None')

    def before_action():
        if runtime.use_stone_auto:
            if runtime.used_stone_count >= runtime.use_stone_max:
                print('\n\n已到达预设的可用理智上限, 脚本将退出')
                exit(0)
            else:
                runtime.used_stone_count += 1
        else:
            print('理智不足，自动退出脚本')
            exit(0)

    return Scene('exchange_intellect_by_stone.png', prefix,
                 before_action=before_action,
                 action_image="exchange_intellect_confirm.png")


def load_scenes(prefix, runtime):
    return [
        prts_disable_detection(prefix),  # 战斗关卡确认出击
        account_upgrade_detection(prefix),  # 战斗结束后账号等级提升
        level_info_detection(prefix),  # 战斗关卡确认出击
        level_team_detection(runtime, prefix),  # 战斗前队伍预览
        level_finish_detection(runtime, prefix),  # 战斗结束后账号等级提升
        prts_running_scene(prefix),  # 副本还在进行中
        exchange_intellect_by_pharmacy(runtime, prefix),  # 理智不足时有可使用的药剂
        exchange_intellect_by_stone(runtime, prefix),  # 理智不足时有可使用的石头
    ]
