# import sys
# sys.path.insert(1, '../common')
from common.scene import Scene
import time


def map_move_spec_question_mark(prefix=''):
    return Scene("explore_map_question_mark.png", prefix,
                 name='地图探索点（问号）',
                 action_tap_offset_y=50)


def battle_fighting(prefix=''):
    def after_action():
        print('.', sep='', end='')

    return Scene("stop_auto_battle_detection.png", prefix,
                 action_tap=False,  # 战斗进行中，不需要点击
                 after_action=after_action)


def strike_confirm(prefix=''):
    return Scene("safe_lane.png", prefix, action_image="choose_level_go_now_button.png")


def choose_team(config, variables, prefix=''):
    def before_action():
        if 0 < variables.repeated_count <= config.repeat_count_max:
            print('\n\n预设的复读次数已完成')
            exit(0)
        variables.repeated_count += 1
        variables.swipe_mode = 0
        if variables.flag_start_printed:
            pass
        else:
            print('\n第 %03d 次副本' % variables.repeated_count, sep='', end='')
            variables.flag_start_printed = True

    return Scene("team_choose.png", prefix,
                 before_action=before_action,
                 action_image="choose_level_go_now_button.png")


def battle_prepare(prefix=''):
    return Scene("battle_prepare.png", prefix, action_image="battle_preview_start_button.png")


def battle_post_view_new_character_confirmation(prefix=''):
    return Scene("battle_post_new_character_detection.png", prefix,
                 name='战役获得SR(或以上)级别角色',
                 action_tap_offset_y=-100)


def difficult_medium(prefix=''):
    return Scene("difficult_medium.png", prefix,
                 action_tap_offset_x=40, action_tap_offset_y=30, threshold=0.7)


def target_not_found(prefix=''):
    return Scene("target_not_found.png", prefix, action_swipe=True, action_tap=False)


def battle_finished(prefix):
    def after_action():
        time.sleep(5)
    return Scene("battle_post_confirm_detection.png", prefix=prefix,
                 action_image="battle_post_confirm_button.png",
                 after_action=after_action)


def wife_unhappy(prefix):
    def before_action():
        exit(0)
    return Scene("wife_unhappy.png", prefix=prefix,
                 action_tap=False,
                 before_action=before_action)


def shipyard_full(prefix):
    def before_action():
        exit(0)
    return Scene("shipyard_full.png", prefix=prefix,
                 action_tap=False,
                 before_action=before_action)


def load_scenes(prefix, config, variables):
    return [
        # wife_unhappy(prefix),  # this is most important.
        Scene("info_box_detection.png", prefix=prefix, action_image="cross_close_button.png"),
        # 索敌开始
        Scene("boss_icon_detection2.png", prefix=prefix, threshold=0.7),
        Scene("enemy_level.png", prefix=prefix, threshold=0.6, action_tap_offset_y=-60),
        difficult_medium(prefix),
        Scene("map_ship_type_1.png", prefix=prefix),  # 判断侦查舰队
        Scene("map_ship_type_2.png", prefix=prefix),  # 判断航母舰队
        Scene("map_ship_type_3.png", prefix=prefix),  # 判断主力舰队
        Scene("map_ship_type_4.png", prefix),  # 判断侦查舰队
        # map_move_spec_question_mark(prefix),
        # 索敌结束
        target_not_found(prefix),
        Scene("ambush_encountered_detection.png", prefix=prefix, action_image="map_move_evade_ambush.png"),

        Scene("battle_" + config.battle_no + '.png', prefix=prefix),
        strike_confirm(prefix),
        choose_team(config, variables, prefix),
        Scene("special_operation_enable_warn.png", prefix=prefix, action_image="confirm.png"),
        Scene("battle_prepare.png", prefix=prefix, action_image="battle_preview_start_button.png"),
        # shipyard_full(prefix),
        Scene("not_auto_fighting_detection.png", prefix=prefix),
        Scene("auto_battle_warning_detection.png", prefix=prefix, action_image="auto_battle_confirm_button.png"),
        battle_fighting(prefix),
        Scene("battle_post_view_s_level.png", prefix=prefix),
        Scene("battle_post_view_get_items_detection.png", prefix=prefix),
        battle_post_view_new_character_confirmation(prefix),
        Scene("whether_locking_this_ship_detection.png", prefix=prefix, action_image="ship_lock_yes_button.png"),
        battle_finished(prefix),

        Scene("now_loading.png", prefix=prefix, action_tap=False)
    ]
