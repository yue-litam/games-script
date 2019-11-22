# coding: utf-8

import time

# import sys
# sys.path.insert(1, '../')

try:
    from common import tool
    from common.scene import Scene
except Exception as importEx:
    print(importEx)
    exit(1)


class EventLoop:
    scenes = None
    device = None
    runtime = None

    def __init__(self, scenes, device, runtime=None):
        self.scenes = scenes
        self.runtime = runtime
        self.device = device

    def execute_tap_action(self, template, img, x_offset=0, y_offset=0):
        touch_loc, _, w, h = tool.device_detect_feature_location_handler(template, img)
        x, y = ((touch_loc[0] + w / 2 + x_offset), (touch_loc[1] + h / 2 + y_offset))
        # print("Touching {0}, {1}".format(x, y))
        self.device.tap_handler(x, y)

    def recognize_and_process_page(self):
        screen = self.device.screen_capture_handler()
        if screen is None:
            return

        # 场景匹配
        ss = None
        for scene in self.scenes:
            if tool.get_similarity(scene.imageTemplate, screen, scene.threshold) == 1:
                ss = scene
                break
        if ss is None:
            return

        # 场景匹配成功后
        self.__debug('match scene {}'.format(ss.name))

        # 前置处理
        if ss.before_action is not None:
            ss.before_action()

        # 需要点击
        if ss.action_tap:
            x0, y0 = tool.find_click_position(ss.actionTemplate, screen)
            x = x0 + ss.action_tap_offset_x
            y = y0 + ss.action_tap_offset_y
            self.__debug('calculate tap position: {0}, {1}'.format(x, y))
            self.device.tap_handler(x, y)

        # 后置处理
        if ss.after_action is not None:
            ss.after_action()

    def start(self):
        while True:
            self.recognize_and_process_page()
            time.sleep(1)

    def __debug(self, message):
        if self.runtime is not None and self.runtime.log_level == 'debug':
            print(message)
