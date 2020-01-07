# coding: utf-8

import time
from logutil import logger
try:
    from common import tool
    from common.scene import Scene
except Exception as importEx:
    logger.error(importEx)
    exit(1)


class EventLoop:
    scenes = None
    device = None
    vars = None

    def __init__(self, scenes, device, variables=None):
        self.scenes = scenes
        self.device = device
        self.vars = variables

    def recognize_and_process_page(self):
        screen = self.device.screen_capture_handler()
        if screen is None:
            return

        # 场景匹配
        matched = None
        for scene in self.scenes:
            if scene.matched_in(screen):
                matched = scene
                logger.debug('match scene {}'.format(matched.name))
                break
        if matched is None:
            logger.debug('当前屏幕无法识别出任何已知匹配的场景')
            return

        # 前置处理
        if matched.before_action is not None:
            matched.before_action(self.device, screen)

        if matched.perform_what() == 'tap':
            # 需要点击
            x, y = matched.where_to_tap(screen)
            logger.debug('calculate tap position: {0}, {1}'.format(x, y))
            self.device.tap_handler(x, y)
        elif matched.perform_what() == 'swipe':
            # 需要手势滑动
            from_x, from_y, to_x, to_y = matched.how_to_swipe()
            self.device.swipe_handler(from_x, from_y, to_x, to_y, 500)

        # 后置处理
        if matched.after_action is not None:
            matched.after_action(self.device, screen)

    def start(self, pause=1):
        while True:
            self.recognize_and_process_page()
            time.sleep(pause)
