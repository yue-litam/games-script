# coding: utf-8

import wda
import cv2

from eventloop import EventLoop

screen_path = 'temp/screen.png'


class IOSEventLoop(EventLoop):
    client = None
    session = None

    def __init__(self, prefix):
        super().__init__(prefix)

        # c = wda.Client('http://192.168.3.101:8100')
        # 如果使用了WDA安装过程中提到的"libimobiledevice"进行端口转发，则替换为http://localhost:8100
        self.client = wda.Client()
        self.session = self.client.session()

        # 获取一张当前手机的截图
        _ = self.client.screenshot(screen_path)
        screen = cv2.imread(screen_path, 0)
        width, height = screen.shape[::-1]
        print("\nScreenWidth: {0}, ScreenHeight: {1}\n".format(width, height))

    def take_screen_shot_handler(self):
        _ = self.client.screenshot(screen_path)
        img = cv2.imread(screen_path, 0)
        return img

    def device_tap_handler(self, pos_x, pos_y):
        self.session.tap(pos_x, pos_y)
