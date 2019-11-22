# import sys
# sys.path.insert(1, '../common')
from common.scene import Scene


def map_move_spec_question_mark(prefix=''):
    return Scene("explore_map_question_mark.png", prefix,
                 name='地图探索点（问号）',
                 action_tap_offset_y=50)


def battle_in_good_state(prefix=''):
    def after_action(_1, _2):
        print('.', sep='', end='')

    return Scene("stop_auto_battle_detection.png", prefix,
                 action_tap=False,  # 战斗进行中，不需要点击
                 after_action=after_action)


def battle_post_view_new_character_confirmation(device=None, prefix='', _=None):
    return Scene("battle_post_new_character_detection.png", prefix,
                 name='战役获得SR(或以上)级别角色',
                 action_tap_offset_y=200)


def load_scenes(prefix, runtime):
    return [
        map_move_spec_question_mark(),
        battle_in_good_state(),
        battle_post_view_new_character_confirmation(),
        Scene("battle_" + runtime.battle_no + '.png', prefix),
        Scene("choose_level_go_now_button.png", prefix),
        Scene("battle_prepare.png", prefix=prefix, action_image="battle_preview_start_button.png"),
        Scene("not_auto_fighting_detection.png", prefix),
        Scene("auto_battle_warning_detection.png", prefix=prefix, action_image="auto_battle_confirm_button.png"),
        Scene("whether_locking_this_ship_detection.png", prefix=prefix, action_image="ship_lock_yes_button.png"),
        Scene("ambush_encountered_detection.png", prefix=prefix, action_image="map_move_evade_ambush.png"),
        Scene("boss_icon_detection.png", prefix),
        Scene("map_ship_type_4.png", prefix),  # 判断运输舰队
        Scene("map_ship_type_1.png", prefix),  # 判断侦查舰队
        Scene("map_ship_type_2.png", prefix),  # 判断航母舰队
        Scene("map_ship_type_3.png", prefix),  # 判断主力舰队
        Scene("battle_post_view_s_level.png", prefix),
        Scene("battle_post_view_get_items_detection.png", prefix),
        Scene("battle_post_confirm_detection.png", prefix, action_image="battle_post_confirm_button.png"),
        Scene("info_box_detection.png", prefix=prefix, action_image="cross_close_button.png")
    ]
