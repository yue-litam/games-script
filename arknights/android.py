# coding: utf-8

import cv2
import numpy
import sys
import os
import subprocess

from io import StringIO
from PIL import ImageFile, Image

sys.path.insert(1, '../common')

try:
    from arknights.eventloop import EventLoop
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

screen_name = 'screen.png'
screen_path = 'temp/' + screen_name
ImageFile.LOAD_TRUNCATED_IMAGES = True


class AndroidEventLoop(EventLoop):
    # SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
    SCREENSHOT_WAY = 3
    adb = None

    def __init__(self):
        super().__init__()

        self.adb = auto_adb()
        self.adb.test_device()
        self.check_screenshot()
        x, y = self.adb.get_size()
        print("ScreenWidth: {0}, ScreenHeight: {1}".format(x, y))

    def check_screenshot(self):
        if os.path.isfile(screen_path):
            # noinspection PyBroadException
            try:
                os.remove(screen_path)
            except Exception:
                pass
        if self.SCREENSHOT_WAY < 0:
            print('暂不支持当前设备')
            sys.exit()
        try:
            im = self.pull_screenshot()
            im.load()
            im.close()
            print('采用方式 {} 获取截图'.format(self.SCREENSHOT_WAY))
        except Exception as pssEx:
            print(pssEx)
            self.SCREENSHOT_WAY -= 1
            self.check_screenshot()

    def pull_screenshot(self):

        if 1 <= self.SCREENSHOT_WAY <= 3:
            process = subprocess.Popen(
                self.adb.adb_path + ' shell screencap -p',
                shell=True, stdout=subprocess.PIPE)
            binary_screenshot = process.stdout.read()
            if self.SCREENSHOT_WAY == 2:
                binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
            elif self.SCREENSHOT_WAY == 1:
                binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
            return Image.open(StringIO(binary_screenshot))
        elif self.SCREENSHOT_WAY == 0:
            self.adb.run('shell screencap -p /sdcard/' + screen_name)
            self.adb.run('pull /sdcard/' + screen_name + ' ./' + screen_path)
            return Image.open('./' + screen_path)

    def take_screen_shot_handler(self):
        screen = self.pull_screenshot()
        img = cv2.cvtColor(numpy.asarray(screen), cv2.COLOR_RGB2GRAY)
        return img

    def device_tap_handler(self, pos_x, pos_y):
        self.adb.run('shell input tap {} {}'.format(pos_x, pos_y))
