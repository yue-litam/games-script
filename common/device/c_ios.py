# coding: utf-8

import cv2
import numpy as np
import wda

from common.device.i_device import Device
from common.logutil import logger
from common.runtime import Config


class IOSDevice(Device):
    client = None
    session = None
    dpi = 1  # iphone SE 的屏幕DPI为2，使用wda发送触摸指令时坐标(x,y)需要除以相应的dpi

    def __init__(self, cfg=None, address='http://127.0.0.1:8100'):
        self.client = wda.Client(address)
        self.session = self.client.session()
        self.dpi = self.session.scale
        x, y = self.session.window_size()
        self.screen_x, self.screen_y = x * self.dpi, y * self.dpi
        self.cfg = cfg if cfg is not None else Config()

    def screen_capture_handler(self, gray=True):
        # 获取一张当前手机的截图
        save_file_name = None
        if self.cfg.screenshot_to_disk and \
                self.cfg.screenshot_to_disk_file_name != '':
            save_file_name = self.cfg.screenshot_to_disk_file_name
        screen = np.asarray(self.client.screenshot(save_file_name))
        # 直接使用截屏方法返回的图像三通道为BGR
        if gray:
            # 返回灰度图
            return cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        else:
            # 翻转为RGB顺序
            return cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    def tap_handler(self, pos_x, pos_y):
        x = pos_x / self.dpi
        y = pos_y / self.dpi
        logger.debug('actually tap position: {0}, {1}'.format(x, y))
        self.session.tap(x, y)

    def swipe_handler(self, from_x, from_y, to_x, to_y, millisecond):
        from_x = int(from_x / self.dpi) if from_x > 0 else 0
        from_y = int(from_y / self.dpi) if from_y > 0 else 0
        to_x = int(to_x / self.dpi) if to_x > 0 else 0
        to_y = int(to_y / self.dpi) if to_y > 0 else 0
        duration = millisecond / 1000  # wda accept duration with 'second' timeunit
        logger.debug('actually swipe from ({0}, {1}) to ({2}, {3})'.format(from_x, from_y, to_x, to_y))
        self.session.swipe(from_x, from_y, to_x, to_y, duration)
