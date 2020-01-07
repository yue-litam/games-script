from logutil import logger
from common.scene import Scene
from common.tool import *
from azurelane.scenes.enemy_search import EnemySearch
import time


def battle_fighting(prefix):
    s = Scene("检测战斗进行时",
              identify_image=load_resource("stop_auto_battle_detection.png", prefix),
              action_type='none',  # 不需要点击
              )
    s.after_action = lambda _1, _2: print('.', sep='', end='')
    return s


def battle_strike_confirm(prefix):
    return Scene("检测指定关卡出击确认",
                 identify_image=load_resource("safe_lane.png", prefix),
                 tap_image=load_resource("choose_level_go_now_button.png", prefix))


def battle_team_choose(config, variables, prefix):
    def before_action(_1, _2):
        if 0 <= config.repeat_count_max <= variables.repeated_count:
            logger.info('预设的复读次数已完成')
            exit(0)
        variables.repeated_count += 1
        variables.round_count = 0
        variables.swipe_mode = 0
        logger.info('\n第 %03d 次副本' % variables.repeated_count)

    s = Scene("检测指定关卡出击队伍选择",
              identify_image=load_resource("team_choose.png", prefix),
              tap_image=load_resource("choose_level_go_now_button.png", prefix))
    s.before_action = before_action
    return s


def battle_prepare(variables, prefix):
    def before_action(_1, _2):
        variables.round_count += 1
        print(variables.round_count, end='', sep='')

    s = Scene("检测出击队伍阵型调整",
              identify_image=load_resource("battle_prepare.png", prefix),
              tap_image=load_resource("battle_preview_start_button.png", prefix))
    s.before_action = before_action
    return s


def battle_finished_evaluation(prefix):
    return Scene("检测战斗完成评价（S/A/B/C）界面",
                 identify_image=load_resource("battle_post_view_s_level.png", prefix))


def battle_finished_item_list_check(prefix):
    return Scene("检测战斗完成道具获得界面",
                 identify_image=load_resource("battle_post_view_get_items_detection.png", prefix))


def battle_finished_super_rare_character_confirm(prefix):
    return Scene('检测获得稀有及以上级别角色',
                 identify_image=load_resource("battle_post_new_character_detection.png", prefix),
                 tap_offset_y=-100)


def battle_finished_lock_new_character(prefix):
    return Scene('检测锁定新角色提示',
                 identify_image=load_resource("lock_ship_detection.png", prefix),
                 tap_image=load_resource("ship_lock_yes_button.png", prefix),
                 tap_offset_y=-100)


def battle_finished_team_exp(prefix):
    s = Scene("检测战斗完成经验结算界面",
              identify_image=load_resource("battle_post_confirm_detection.png", prefix),
              tap_image=load_resource("battle_post_confirm_button.png", prefix))
    return s


def wife_unhappy(prefix):
    def before_action(_1, _2):
        logger.info('队伍存在舰娘心情警告，指挥官休息一下吧')
        exit(0)

    s = Scene("检测舰娘心情值偏低",
              identify_image=load_resource("unhappy.png", prefix))
    s.before_action = before_action
    return s


def shipyard_full(prefix):
    def before_action():
        logger.info('船坞满了，指挥官清理一下喵')
        exit(0)

    s = Scene("检测船坞已满提示",
              identify_image=load_resource("shipyard_full.png", prefix))
    s.before_action = before_action
    return s


def battle_auto_fight_enable(prefix):
    return Scene("检测自律战斗未开启",
                 identify_image=load_resource("not_auto_fighting_detection.png", prefix))


def battle_auto_fight_warning(prefix):
    return Scene("检测自律战斗警告提示",
                 identify_image=load_resource("auto_battle_warning_detection.png", prefix),
                 tap_image=load_resource("auto_battle_confirm_button.png", prefix))


def close_simple_info_box(prefix):
    return Scene("检测普通提示框",
                 identify_image=load_resource("info_box_detection.png", prefix),
                 tap_image=load_resource("cross_close_button.png", prefix))


def evade_ambush(prefix):
    return Scene("检测命中伏击舰队（bad luck）",
                 identify_image=load_resource("ambush_encountered_detection.png", prefix),
                 tap_image=load_resource("map_move_evade_ambush.png", prefix))


def battle_entry(entry_name, prefix):
    return Scene("检测自律关卡入口",
                 identify_image=load_resource("battle_" + entry_name + '.png', prefix))


def battle_special_info(prefix):
    return Scene("检测特别行动开启提示",
                 identify_image=load_resource("special_operation_enable_warn.png", prefix),
                 tap_image=load_resource("confirm.png", prefix))


def enemy_search(prefix, variables):
    return EnemySearch("开始索敌",
                       load_resource("fallback_and_switch_btn.png", prefix),
                       variables)


def load_scenes(prefix, config, variables):
    return [
        wife_unhappy(prefix),  # this is most important!
        shipyard_full(prefix),
        battle_auto_fight_enable(prefix),
        battle_auto_fight_warning(prefix),
        close_simple_info_box(prefix),

        battle_entry(config.battle_no, 'azurelane/assets/select_battle_feature/'),
        battle_strike_confirm(prefix),
        battle_team_choose(config, variables, prefix),
        battle_special_info(prefix),
        evade_ambush(prefix),
        enemy_search(prefix, variables),  # 索敌

        battle_prepare(variables, prefix),
        battle_fighting(prefix),
        battle_finished_evaluation(prefix),
        battle_finished_item_list_check(prefix),
        battle_finished_super_rare_character_confirm(prefix),
        battle_finished_lock_new_character(prefix),
        battle_finished_team_exp(prefix)
    ]
