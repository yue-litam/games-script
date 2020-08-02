import time

from common.logutil import logger
from common.scene import Scene
from common.tool import *
from ext.serverchan import program_exit_alert
from games.azurelane.scenes.enemy_search import EnemySearch


def battle_fighting(prefix):
    s = Scene("检测战斗进行时",
              identify_image=load_resource("stop_auto_battle_detection.png", prefix),
              action_type='none',  # 不需要点击
              )
    return s


def battle_safe_lane_strike_confirm(prefix):
    return Scene("检测指定关卡出击确认",
                 # identify_image=load_resource("choose_level_go_now_button.png", prefix),
                 identify_image=load_resource("safe_lane.png", prefix),
                 tap_image=load_resource("choose_level_go_now_button.png", prefix))


def battle_danger_lane_strike_confirm(prefix):
    return Scene("检测指定关卡出击确认",
                 # identify_image=load_resource("choose_level_go_now_button.png", prefix),
                 identify_image=load_resource("danger_lane.png", prefix),
                 tap_image=load_resource("choose_level_go_now_button.png", prefix))


def battle_highly_danger_lane_strike_confirm(prefix):
    return Scene("检测指定关卡出击确认",
                 # identify_image=load_resource("choose_level_go_now_button.png", prefix),
                 identify_image=load_resource("highly_danger_lane.png", prefix),
                 tap_image=load_resource("choose_level_go_now_button.png", prefix))


def battle_team_choose(config, context, prefix):
    def before_action(_1, _2):
        if 0 <= config.repeat_count_max <= context.repeated_count:
            print()
            cause = "预设的复读次数已完成"
            logger.info(cause)
            program_exit_alert(cause)
            exit(0)
        context.repeated_count += 1
        context.round_count = 0
        context.swipe_mode = config.default_swipe_direction
        print('')
        logger.info('第 %03d 次副本' % context.repeated_count)

    s = Scene("检测指定关卡出击队伍选择",
              identify_image=load_resource("team_choose.png", prefix),
              tap_image=load_resource("choose_level_go_now_button.png", prefix))
    s.before_action = before_action
    s.after_action = lambda _1, _2: time.sleep(5)
    return s


def battle_prepare(context, prefix):
    def before_action(_1, _2):
        context.round_count += 1
        print('%s 次出击' % context.round_count, end=',', sep='', flush=True)

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
    s = Scene('检测锁定新角色提示',
              identify_image=load_resource("lock_ship_detection.png", prefix),
              tap_image=load_resource("ship_lock_yes_button.png", prefix),
              tap_offset_y=-100)
    s.after_action = lambda _1, _2: logger.info("  new character locked!")
    return s


def battle_finished_team_exp(prefix):
    s = Scene("检测战斗完成经验结算界面",
              identify_image=load_resource("battle_post_confirm_detection.png", prefix),
              tap_image=load_resource("battle_post_confirm_button.png", prefix))
    s.after_action = lambda _1, _2: time.sleep(5)
    return s


def wife_unhappy(prefix, context):
    def before_action(_1, _2):
        print()
        cause = "队伍存在舰娘心情警告，指挥官休息一下吧，已出击" + str(context.repeated_count) + "次"
        logger.info(cause)
        program_exit_alert(cause)
        exit(0)

    s = Scene("检测舰娘心情值偏低",
              identify_image=load_resource("unhappy.png", prefix))
    s.before_action = before_action
    return s


def shipyard_full(prefix, context):
    def before_action(_1, _2):
        print()
        cause = "船坞满了，指挥官清理一下喵，已出击" + str(context.repeated_count) + "次"
        logger.info(cause)
        program_exit_alert(cause)
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


def enemy_search(prefix_scene, prefix, config, context):
    return EnemySearch("开始索敌",
                       load_resource("fallback_and_switch_btn.png", prefix_scene),
                       context, config, prefix)


def use_special_ticket(prefix):
    return Scene("特别行动:战斗!皇家女仆队2",
                 identify_image=load_resource("use_special_ticket.png", prefix),
                 tap_image=load_resource("use.png", prefix))


def load_scenes(prefix, config, context):
    prefix_scene = prefix + "scenes_feature/"
    prefix_battle = prefix + "select_battle_feature/"
    prefix_target = prefix + "search_ship_feature/"
    return [
        wife_unhappy(prefix_scene, context),  # this is most important!
        shipyard_full(prefix_scene, context),
        battle_auto_fight_enable(prefix_scene),
        battle_auto_fight_warning(prefix_scene),
        use_special_ticket(prefix_scene),
        close_simple_info_box(prefix_scene),

        battle_entry(config.battle_no, prefix_battle),
        battle_safe_lane_strike_confirm(prefix_scene),
        battle_danger_lane_strike_confirm(prefix_scene),
        battle_highly_danger_lane_strike_confirm(prefix_scene),
        battle_team_choose(config, context, prefix_scene),
        battle_special_info(prefix_scene),
        evade_ambush(prefix_scene),

        battle_prepare(context, prefix_scene),
        battle_fighting(prefix_scene),
        battle_finished_evaluation(prefix_scene),
        battle_finished_item_list_check(prefix_scene),
        battle_finished_super_rare_character_confirm(prefix_scene),
        battle_finished_lock_new_character(prefix_scene),
        battle_finished_team_exp(prefix_scene),

        enemy_search(prefix_scene, prefix, config, context)  # 索敌
    ]
