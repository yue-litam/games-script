# coding: utf-8

import time
import sys

sys.path.insert(1, '../common')

try:
    from common import tool
    from common.scene import Scene
except Exception as importEx:
    print(importEx)
    exit(1)


class EventLoop:
    scenes = None

    def __init__(self):
        pass

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
