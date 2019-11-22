# coding: utf-8

import time
import sys
from configparser import ConfigParser

sys.path.insert(1, '../')

try:
    from common import tool
    from common.scene import Scene
    from loadscenes import *
    from runtime import Runtime
except Exception as importEx:
    print(importEx)
    exit(1)


class EventLoop:
    scenes = None
    runtime = None

    def __init__(self, prefix=''):
        cfg = ConfigParser()
        rt = Runtime()
        try:
            cfg.read('config.ini')
            rt.use_stone_auto = cfg.getboolean('intellect', 'use_stone')
            rt.use_stone_max = cfg.getint('intellect', 'use_stone_max')
            rt.use_pharmacy_auto = cfg.getboolean('intellect', 'use_pharmacy')
            rt.use_pharmacy_max = cfg.getint('intellect', 'use_pharmacy_max')
            print('理智不足时')
            print('\t自动使用药剂:{0}, 最多使用数量:{1}'.format(rt.use_pharmacy_auto, rt.use_pharmacy_max))
            print('\t自动使用石头:{0}, 最多使用数量:{1}'.format(rt.use_stone_auto, rt.use_stone_max))
            print('')
        except Exception as ex:
            print(ex)

        self.runtime = rt
        self.scenes = [
            prts_disable_detection(self, prefix),  # 战斗关卡确认出击
            account_upgrade_detection(self, prefix),  # 战斗结束后账号等级提升
            level_info_detection(self, prefix),  # 战斗关卡确认出击
            level_team_detection(self, prefix),  # 战斗前队伍预览
            level_finish_detection(self, prefix),  # 战斗结束后账号等级提升
            prts_running_scene(self, prefix),  # 副本还在进行中
            exchange_intellect_by_pharmacy(self, prefix),  # 理智不足时有可使用的药剂
            exchange_intellect_by_stone(self, prefix),  # 理智不足时有可使用的石头
        ]

    def take_screen_shot_handler(self):
        raise NotImplementedError("Should have implemented this: 截屏方法")

    def device_tap_handler(self, pos_x, pos_y):
        raise NotImplementedError("Should have implemented this: 触摸屏幕指令方法")

    def execute_tap_action(self, template, img, x_offset=0, y_offset=0):
        touch_loc, _, w, h = tool.device_detect_feature_location_handler(template, img)
        x, y = ((touch_loc[0] + w / 2 + x_offset), (touch_loc[1] + h / 2 + y_offset))
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
