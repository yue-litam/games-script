# coding: utf-8

import wda
import cv2

from common.device.i_device import Device

screen_path = 'temp/screen.png'


class IOSDevice(Device):
    client = None
    session = None
    dpi = 1

    def __init__(self, dpi=1, log_level=None, address='http://127.0.0.1:8100'):
        super().__init__(log_level)

        self.client = wda.Client(address)
        self.session = self.client.session()
        self.dpi = dpi

        # 获取一张当前手机的截图
        _ = self.client.screenshot(screen_path)
        screen = cv2.imread(screen_path, 0)
        width, height = screen.shape[::-1]
        print("\nScreenWidth: {0}, ScreenHeight: {1}\n".format(width, height))

    def screen_capture_handler(self, file_name=''):
        if file_name == '':
            file_name = screen_path
        _ = self.client.screenshot(file_name)
        img = cv2.imread(file_name, 0)
        return img

    def tap_handler(self, pos_x, pos_y):
        x = pos_x / self.dpi
        y = pos_y / self.dpi
        super().debug('actually tap position: {0}, {1}'.format(x, y))
        self.session.tap(x, y)

    def swipe_handler(self, from_x, from_y, to_x, to_y, millisecond):
        raise NotImplementedError("Should have implemented this: 单击并按住拖动屏幕指令方法")
