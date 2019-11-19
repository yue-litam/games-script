# coding: utf-8

import time
import sys
from configparser import ConfigParser

sys.path.insert(1, '../common')

try:
    import tool
    from scene import Scene
except Exception as importEx:
    print(importEx)
    exit(1)


class EventLoop:
    scenes = []
    round_count = 0
    assets_prefix = ''
    battle_no = '3_1'

    def __init__(self, assets_prefix):

        cfg = ConfigParser()
        try:
            cfg.read('config.ini')
            self.battle_no = cfg.get('battle', 'battle_no')
        except Exception as initEx:
            print(initEx)
            exit(1)

        def map_move_spec_question_mark():
            def f(template, img):
                self.tap(template, img, 0, 50)

            return Scene("explore_map_question_mark.png", f, "explore_map_question_mark.png", assets_prefix)

        def battle_in_good_state():
            def f(_1, _2):
                print('.', sep='', end='')
                pass

            return Scene("stop_auto_battle_detection.png", f, None, assets_prefix)

        def battle_post_view_new_character_confirmation():
            def f(template, img):
                self.tap(template, img, 0, 200)

            return Scene("battle_post_new_character_detection.png", f, None, assets_prefix)

        self.scenes = [
            Scene("battle_" + self.battle_no + '.png', self.tap, None, assets_prefix),
            Scene("choose_level_go_now_button.png", self.tap, None, assets_prefix),
            Scene("battle_prepare.png", self.tap, "battle_preview_start_button.png", assets_prefix),
            Scene("not_auto_fighting_detection.png", self.tap, None, assets_prefix),
            Scene("auto_battle_warning_detection.png", self.tap, "auto_battle_confirm_button.png", assets_prefix),
            battle_post_view_new_character_confirmation(),
            Scene("whether_locking_this_ship_detection.png", self.tap, "ship_lock_yes_button.png", assets_prefix),
            Scene("ambush_encountered_detection.png", self.tap, "map_move_evade_ambush.png", assets_prefix),
            Scene("boss_icon_detection.png", self.tap, "boss_icon_detection.png", assets_prefix),
            Scene("map_ship_type_4.png", self.tap, None, assets_prefix),  # 判断运输舰队
            Scene("map_ship_type_1.png", self.tap, None, assets_prefix),  # 判断侦查舰队
            Scene("map_ship_type_2.png", self.tap, None, assets_prefix),  # 判断航母舰队
            Scene("map_ship_type_3.png", self.tap, None, assets_prefix),  # 判断主力舰队
            map_move_spec_question_mark(),
            Scene("battle_post_view_s_level.png", self.tap, None, assets_prefix),
            Scene("battle_post_view_get_items_detection.png", self.tap, None, assets_prefix),
            Scene("battle_post_confirm_detection.png", self.tap, "battle_post_confirm_button.png", assets_prefix),
            battle_in_good_state(),
            Scene("info_box_detection.png", self.tap, "cross_close_button.png", assets_prefix)
        ]

    def take_screen_shot_handler(self):
        raise NotImplementedError("Should have implemented this: 截屏方法")

    def device_tap_handler(self, pos_x, pos_y):
        raise NotImplementedError("Should have implemented this: 触摸屏幕指令方法")

    def tap(self, template, img, x_offset=0, y_offset=0):
        touch_loc, _, w, h = tool.device_detect_feature_location_handler(template, img)
        x, y = ((touch_loc[0] + w / 2 + x_offset) / 2, (touch_loc[1] + h / 2 + y_offset) / 2)
        # print("Touching {0}, {1}".format(x, y))
        self.device_tap_handler(x, y)

    def recognize_and_process_page(self):
        img = self.take_screen_shot_handler()
        if img is None:
            return

        ss = None
        for scene in self.scenes:
            match = tool.get_similarity(scene.imageTemplate, img, scene) == 1
            if match:
                ss = scene
                break
        if ss is None:
            # print('?', sep='', end='')
            # print('unable recognize scene, wait for next time.')
            return

        scene_name = ss.image_name
        filtered = [s for s in self.scenes if s.image_name == ss.image_name]

        ss = None
        for scene in filtered:
            match = tool.get_similarity(scene.actionTemplate, img, scene) == 1
            if match:
                ss = scene
                break
        if ss is None:
            print('scene', scene_name, ' unable recognize action feature.')
        else:
            ss.action(ss.actionTemplate, img)

    def start(self):
        while True:
            self.recognize_and_process_page()
            time.sleep(1)
