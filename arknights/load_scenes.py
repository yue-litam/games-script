import time

from common.logutil import logger
from common.scene import Scene
from common.tool import load_resource


def account_upgrade_detection(prefix):
    return Scene('检测账号升级',
                 identify_image=load_resource('account_upgrade_detection.png', prefix))


def prts_disable_detection(prefix):
    return Scene('检测自律未打开', identify_image=load_resource('prts_disable_detection.png', prefix))


def level_info_detection(prefix):
    image = load_resource('level_info_detection.png', prefix)
    width, _ = image.shape[::-1]
    return Scene('检测指定关卡信息介绍页面', identify_image=image, tap_offset_x=width)


def annihilation_detection(prefix):
    image = load_resource('annihilation_detection.png', prefix)
    width, _ = image.shape[::-1]
    return Scene('检测剿灭模式关卡信息介绍页面',
                 identify_image=load_resource('annihilation_detection.png', prefix),
                 tap_offset_x=250,
                 tap_offset_y=30)


def annihilation_finish_detection(prefix):
    return Scene('检测剿灭模式自律完成页面', identify_image=load_resource('annihilation_finish_detection.png', prefix))


def prts_running_scene(prefix):
    s = Scene('检测自律战斗进行中', action_type='none',
              identify_image=load_resource('level_fighting_detection.png', prefix))
    return s


def level_team_detection(config, context, prefix):
    def before_action(_1, _2):
        if 0 <= config.repeat_count_max <= context.repeated_count:
            logger.info('\n\n预设的复读次数已完成')
            exit(0)
        context.repeated_count += 1
        logger.info('第 %03d 次副本' % context.repeated_count)

    s = Scene('检测指定关卡自律队伍阵容页面',
              identify_image=load_resource('level_team_detection.png', prefix))
    s.before_action = before_action
    s.after_action = lambda _1, _2: time.sleep(2)
    return s


def level_finish_detection(context, prefix):
    def after_action(_1, _2):
        context.flag_start_printed = False

    s = Scene('检测指定关卡自律完成页面',
              identify_image=load_resource('level_finish_detection.png', prefix))
    s.after_action = after_action
    return s


def exchange_intellect_by_pharmacy(config, context, prefix):
    def before_action(_1, _2):
        if config.use_pharmacy_max > 0:
            if context.pharmacy_used >= config.use_pharmacy_max:
                logger.info('已到达预设的可用药剂上限, 脚本将退出')
                exit(0)
            else:
                context.pharmacy_used += 1
        else:
            logger.info('理智不足，自动退出脚本')
            exit(0)

    s = Scene('检测建议使用药剂补充理智页面',
              identify_image=load_resource('exchange_intellect_by_pharmacy.png', prefix),
              tap_image=load_resource("exchange_intellect_confirm.png", prefix))
    s.before_action = before_action
    return s


def exchange_intellect_by_stone(config, context, prefix):
    def before_action(_1, _2):
        if config.use_stone_max > 0:
            if context.stone_used >= config.use_stone_max:
                logger.info('已到达预设的可用源石上限, 脚本将退出')
                exit(0)
            else:
                context.stone_used += 1
        else:
            logger.info('理智不足，自动退出脚本')
            exit(0)

    s = Scene('检测建议使用石头补充理智页面',
              identify_image=load_resource('exchange_intellect_by_stone.png', prefix),
              tap_image=load_resource("exchange_intellect_confirm.png", prefix))
    s.before_action = before_action
    return s


def load_scenes(prefix, config, context):
    return [
        prts_disable_detection(prefix),  # 战斗关卡确认出击
        account_upgrade_detection(prefix),  # 战斗结束后账号等级提升
        annihilation_detection(prefix),  # 剿灭确认出击
        annihilation_finish_detection(prefix),  # 剿灭完成
        level_info_detection(prefix),  # 战斗关卡确认出击
        level_team_detection(config, context, prefix),  # 战斗前队伍预览
        level_finish_detection(context, prefix),  # 战斗结束后账号等级提升
        prts_running_scene(prefix),  # 副本还在进行中
        exchange_intellect_by_pharmacy(config, context, prefix),  # 理智不足时有可使用的药剂
        exchange_intellect_by_stone(config, context, prefix),  # 理智不足时有可使用的石头
    ]
