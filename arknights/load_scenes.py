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


def annihilation_detection(prefix=''):
    scene = Scene('annihilation_detection.png', prefix)
    scene.action_tap_offset_x = scene.action_image_w
    return scene


def annihilation_finish_detection(prefix=''):
    return Scene('annihilation_finish_detection.png', prefix)


def prts_running_scene(prefix=''):
    def after_action():
        print('.', sep='', end='')

    return Scene('level_fighting_detection.png', prefix,
                 action_tap=False, after_action=after_action)


def level_team_detection(config, variables, prefix=''):
    def before_action():
        if 0 <= config.repeat_count_max <= variables.repeated_count:
            print('\n\n预设的复读次数已完成')
            exit(0)
        variables.repeated_count += 1
        print('\n第 %03d 次副本' % variables.repeated_count, sep='', end='')
    return Scene('level_team_detection.png', prefix, before_action=before_action)


def level_finish_detection(variables, prefix=''):
    def after_action():
        variables.flag_start_printed = False

    return Scene('level_finish_detection.png', prefix, after_action=after_action)


def exchange_intellect_by_pharmacy(config, variables, prefix=''):
    def before_action():
        if config.use_pharmacy_max > 0:
            if variables.pharmacy_used >= config.use_pharmacy_max:
                print('\n\n已到达预设的可用理智上限, 脚本将退出')
                exit(0)
            else:
                variables.pharmacy_used += 1
        else:
            print('理智不足，自动退出脚本')
            exit(0)

    return Scene('exchange_intellect_by_pharmacy.png', prefix,
                 before_action=before_action,
                 action_image="exchange_intellect_confirm.png")


def exchange_intellect_by_stone(config, variables, prefix=''):
    def before_action():
        if config.use_stone_max > 0:
            if variables.stone_used >= config.use_stone_max:
                print('\n\n已到达预设的可用理智上限, 脚本将退出')
                exit(0)
            else:
                variables.stone_used += 1
        else:
            print('理智不足，自动退出脚本')
            exit(0)

    return Scene('exchange_intellect_by_stone.png', prefix,
                 before_action=before_action,
                 action_image="exchange_intellect_confirm.png")


def load_scenes(prefix, config, variables):
    return [
        prts_disable_detection(prefix),  # 战斗关卡确认出击
        account_upgrade_detection(prefix),  # 战斗结束后账号等级提升
        annihilation_detection(prefix),  # 剿灭确认出击
        annihilation_finish_detection(prefix),  # 剿灭完成
        level_info_detection(prefix),  # 战斗关卡确认出击
        level_team_detection(config, variables, prefix),  # 战斗前队伍预览
        level_finish_detection(variables, prefix),  # 战斗结束后账号等级提升
        prts_running_scene(prefix),  # 副本还在进行中
        exchange_intellect_by_pharmacy(config, variables, prefix),  # 理智不足时有可使用的药剂
        exchange_intellect_by_stone(config, variables, prefix),  # 理智不足时有可使用的石头
    ]
