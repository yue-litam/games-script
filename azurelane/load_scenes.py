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
        if 0 <= config.repeat_count_max <= variables.repeated_count:
            print('\n\n预设的复读次数已完成')
            exit(0)
        variables.repeated_count += 1
        variables.round_count = 0
        variables.swipe_mode = 0
        print('\n第 %03d 次副本' % variables.repeated_count, sep='', end='')
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


def target_not_found(variables, prefix=''):
    def swipe_from_center(device, to_x, to_y):
        width, height = variables.device_screen_width, variables.device_screen_height
        center_x, center_y = width / 2, height / 2  # 屏幕中心坐标
        device.swipe_handler(center_x, center_y, to_x, to_y, 500)

    def swipe_handler(device):
        width, height = variables.device_screen_width, variables.device_screen_height
        center_x, center_y = width / 2, height / 2  # 屏幕中心坐标
        horizontal_unit_distance = width / 3  # 水平方向每次移动距离
        vertical_unit_distance = height / 3  # 垂直方向每次移动距离
        if variables.swipe_mode == 0:
            print('↑', end='', sep='')  # 手势从上往下，查看上侧区域
            swipe_from_center(device, center_x, center_y + vertical_unit_distance)
            variables.swipe_mode = 1  # 下次向右滑动
        elif variables.swipe_mode == 1:
            print('→', end='', sep='')  # 手势从右往左，查看右侧区域
            swipe_from_center(device, center_x - horizontal_unit_distance, center_y)
            variables.swipe_mode = 2  # 下次向下滑动
        elif variables.swipe_mode == 2:
            print('↓', end='', sep='')  # 手势从下往上，查看下侧区域
            swipe_from_center(device, center_x, center_y - vertical_unit_distance * 2)
            variables.swipe_mode = 3  # 下次向左滑动
        else:
            print('←', end='', sep='')  # 手势从左往右，查看左侧区域
            swipe_from_center(device, center_x + horizontal_unit_distance * 2, center_y)
            variables.swipe_mode = 0  # 下次向上滑动
    return Scene("target_not_found.png", prefix,
                 action_swipe=True, swipe_handler=swipe_handler,
                 action_tap=False)


def battle_finished(prefix):
    def after_action():
        time.sleep(5)
    return Scene("battle_post_confirm_detection.png", prefix=prefix,
                 action_image="battle_post_confirm_button.png",
                 after_action=after_action)


def wife_unhappy(prefix):
    def before_action():
        print('队伍存在舰娘心情警告，指挥官休息一下吧')
        exit(0)
    return Scene("unhappy.png", prefix=prefix,
                 action_tap=False,
                 before_action=before_action)


def shipyard_full(prefix):
    def before_action():
        print('船坞满了，指挥官清理一下喵')
        exit(0)
    return Scene("shipyard_full.png", prefix=prefix,
                 action_tap=False,
                 before_action=before_action)


def round_start(variables, prefix):
    def before_action():
        variables.round_count += 1
        print(variables.round_count, end='', sep='')
    return Scene("battle_prepare.png", prefix=prefix,
                 action_image="battle_preview_start_button.png",
                 before_action=before_action)


def load_scenes(prefix, config, variables):
    return [
        wife_unhappy(prefix),  # this is most important.
        shipyard_full(prefix),
        Scene("info_box_detection.png", prefix=prefix, action_image="cross_close_button.png"),
        # 索敌开始
        Scene("boss_icon_detection2.png", prefix=prefix, threshold=0.7),
        Scene("boss_small.png", prefix=prefix, threshold=0.7),
        Scene("enemy_level.png", prefix=prefix, threshold=0.6, action_tap_offset_y=-55),
        difficult_medium(prefix),
        Scene("map_ship_type_1.png", prefix=prefix),  # 判断侦查舰队
        Scene("map_ship_type_2.png", prefix=prefix),  # 判断航母舰队
        Scene("map_ship_type_3.png", prefix=prefix),  # 判断主力舰队
        Scene("map_ship_type_4.png", prefix),  # 判断侦查舰队
        # map_move_spec_question_mark(prefix),
        # 索敌结束
        target_not_found(variables, prefix),
        Scene("ambush_encountered_detection.png", prefix=prefix, action_image="map_move_evade_ambush.png"),

        Scene("battle_" + config.battle_no + '.png', prefix=prefix),
        strike_confirm(prefix),
        choose_team(config, variables, prefix),
        Scene("special_operation_enable_warn.png", prefix=prefix, action_image="confirm.png"),
        round_start(variables, prefix),
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
