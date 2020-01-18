# coding: utf-8

import cv2
import wda

from common.device.i_device import Device
from common.logutil import logger

screen_path = 'temp/screen.png'


class IOSDevice(Device):
    client = None
    session = None
    dpi = 1  # iphone SE 的屏幕DPI为2，使用wda发送触摸指令时坐标(x,y)需要除以相应的dpi

    def __init__(self, dpi=1, address='http://127.0.0.1:8100'):
        self.client = wda.Client(address)
        self.session = self.client.session()
        self.dpi = dpi

        # 获取一张当前手机的截图
        _ = self.client.screenshot(screen_path)
        screen = cv2.imread(screen_path, 0)
        self.screen_x, self.screen_y = screen.shape[::-1]

    def screen_capture_handler(self, file_name=''):
        if file_name == '':
            file_name = screen_path
        _ = self.client.screenshot(file_name)
        img = cv2.imread(file_name, 0)
        return img

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
