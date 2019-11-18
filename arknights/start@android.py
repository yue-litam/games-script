# coding: utf-8

import cv2
import numpy
import sys
import os
import subprocess

from io import StringIO
from PIL import ImageFile, Image
from eventloop import EventLoop

ImageFile.LOAD_TRUNCATED_IMAGES = True
screen_path = 'temp/arknights.png'

try:
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)


class AndroidEventLoop(EventLoop):
    # SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
    SCREENSHOT_WAY = 3
    adb = None

    def __init__(self, assets_path_prefix):
        super().__init__(assets_path_prefix)

        self.adb = auto_adb()
        self.adb.test_device()
        self.check_screenshot()
        x, y = self.adb.get_size()
        print("ScreenWidth: {0}, ScreenHeight: {1}".format(x, y))

    def check_screenshot(self):
        """
        检查获取截图的方式
        """
        global SCREENSHOT_WAY
        SCREENSHOT_WAY = 0
        if os.path.isfile(screen_path):
            # noinspection PyBroadException
            try:
                os.remove(screen_path)
            except Exception:
                pass
        if SCREENSHOT_WAY < 0:
            print('暂不支持当前设备')
            sys.exit()
        # noinspection PyBroadException
        try:
            im = self.pull_screenshot()
            im.load()
            im.close()
            print('采用方式 {} 获取截图'.format(SCREENSHOT_WAY))
        except Exception:
            SCREENSHOT_WAY -= 1
            self.check_screenshot()

    def pull_screenshot(self):

        global SCREENSHOT_WAY
        if 1 <= SCREENSHOT_WAY <= 3:
            process = subprocess.Popen(
                self.adb.adb_path + ' shell screencap -p',
                shell=True, stdout=subprocess.PIPE)
            binary_screenshot = process.stdout.read()
            if SCREENSHOT_WAY == 2:
                binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
            elif SCREENSHOT_WAY == 1:
                binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
            return Image.open(StringIO(binary_screenshot))
        elif SCREENSHOT_WAY == 0:
            self.adb.run('shell screencap -p /sdcard/' + screen_path)
            self.adb.run('pull /sdcard/' + screen_path + ' .')
            return Image.open('./' + screen_path).resize((960, 540))

    def take_screen_shot_handler(self):
        screen = self.pull_screenshot()
        img = cv2.cvtColor(numpy.asarray(screen), cv2.COLOR_RGB2BGR)
        return img

    def device_tap_handler(self, pos_x, pos_y):
        self.adb.run('shell input tap {} {}'.format(pos_x, pos_y))
        self.session.tap(pos_x, pos_y)


if __name__ == '__main__':
    AndroidEventLoop('assets/general/feature/').start()
