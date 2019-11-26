# import sys
# sys.path.insert(1, '../common')
from common.scene import Scene


def map_move_spec_question_mark(prefix=''):
    return Scene("explore_map_question_mark.png", prefix,
                 name='地图探索点（问号）',
                 action_tap_offset_y=50)


def battle_in_good_state(prefix=''):
    def after_action():
        print('.', sep='', end='')

    return Scene("stop_auto_battle_detection.png", prefix,
                 action_tap=False,  # 战斗进行中，不需要点击
                 after_action=after_action)


def choose_level_go_now_button(prefix=''):
    return Scene("choose_level_go_now_button.png", prefix)


def battle_prepare(runtime, prefix=''):
    def before_action():
        runtime.round_count += 1
        print('\n第 %03d 次战斗' % runtime.round_count, sep='', end='')

    return Scene("battle_prepare.png", prefix,
                 action_image="battle_preview_start_button.png",
                 after_action=before_action)


def battle_post_view_new_character_confirmation(prefix=''):
    return Scene("battle_post_new_character_detection.png", prefix,
                 name='战役获得SR(或以上)级别角色',
                 action_tap_offset_y=-100)


def difficult_medium(prefix=''):
    return Scene("difficult_medium.png", prefix,
                 action_tap_offset_x=40, action_tap_offset_y=30, threshold=0.7)


def load_scenes(prefix, runtime):
    return [
        Scene("boss_icon_detection2.png", prefix, threshold=0.7),
        Scene("enemy_level.png", prefix, threshold=0.6),
        difficult_medium(prefix),
        Scene("map_ship_type_1.png", prefix, threshold=0.6),  # 判断侦查舰队
        Scene("map_ship_type_2.png", prefix, threshold=0.6),  # 判断航母舰队
        Scene("map_ship_type_3.png", prefix, threshold=0.6),  # 判断主力舰队
        # Scene("map_ship_type_4.png", prefix, threshold=0.6),  # 判断侦查舰队
        map_move_spec_question_mark(prefix),
        battle_in_good_state(prefix),
        battle_post_view_new_character_confirmation(prefix),
        choose_level_go_now_button(prefix),
        battle_prepare(runtime, prefix),
        Scene("not_auto_fighting_detection.png", prefix),
        Scene("auto_battle_warning_detection.png", prefix=prefix, action_image="auto_battle_confirm_button.png"),
        Scene("whether_locking_this_ship_detection.png", prefix=prefix, action_image="ship_lock_yes_button.png"),
        Scene("ambush_encountered_detection.png", prefix=prefix, action_image="map_move_evade_ambush.png"),
        Scene("battle_post_view_s_level.png", prefix),
        Scene("battle_post_view_get_items_detection.png", prefix),
        Scene("battle_post_confirm_detection.png", prefix, action_image="battle_post_confirm_button.png"),
        Scene("special_operation_enable_warn.png", prefix, action_image="confirm.png"),
        Scene("info_box_detection.png", prefix=prefix, action_image="cross_close_button.png"),
        Scene("battle_" + runtime.battle_no + '.png', prefix),
        Scene("now_loading.png", prefix)
    ]
