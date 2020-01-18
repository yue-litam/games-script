# coding: utf-8

import cv2
import numpy
import sys
import os
import subprocess

from io import StringIO
from PIL import ImageFile, Image
from common.logutil import logger

sys.path.insert(1, '../common')

try:
    from common.device.i_device import Device
    from common.device.adb import Adb
except Exception as ex:
    logger.error(ex)
    logger.error('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

screen_name = 'screen.png'
screen_path = './temp/' + screen_name
ImageFile.LOAD_TRUNCATED_IMAGES = True


class AndroidDevice(Device):
    SCREENSHOT_WAY = 3
    adb = None

    def __init__(self, address=''):
        self.adb = Adb(device=address)
        self.adb.test_device()
        self.__check_screenshot()
        self.screen_x, self.screen_y = self.adb.get_size()

    def tap_handler(self, pos_x, pos_y):
        logger.debug('actually tap position: {0}, {1}'.format(pos_x, pos_y))
        self.adb.run('shell input tap {} {}'.format(pos_x, pos_y))

    def swipe_handler(self, from_x, from_y, to_x, to_y, millisecond):
        self.adb.run('shell input swipe {} {} {} {} {}'.format(from_x, from_y, to_x, to_y, millisecond))

    def screen_capture_handler(self, file_name=''):
        screen = self.__pull_screenshot(file_name)
        img = cv2.cvtColor(numpy.asarray(screen), cv2.COLOR_RGB2GRAY)
        return img

    def screen_capture_as_image(self):
        return self.__pull_screenshot()

    def __check_screenshot(self):
        while True:
            if os.path.isfile(screen_path):
                try:
                    os.remove(screen_path)
                except Exception:
                    pass
            if self.SCREENSHOT_WAY < 0:
                logger.error('暂不支持当前设备')
                sys.exit()
            try:
                im = self.__pull_screenshot()
                im.load()
                im.close()
                logger.info('采用方式 {} 获取截图'.format(self.SCREENSHOT_WAY))
                break
            except Exception as pssEx:
                logger.error(pssEx)
                self.SCREENSHOT_WAY -= 1

    def __pull_screenshot(self, file_name=''):
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
            if file_name == '':
                file_name = screen_path
            self.adb.run('shell screencap -p /sdcard/' + screen_name)
            self.adb.run('pull /sdcard/' + screen_name + ' ' + file_name)
            return Image.open('' + file_name)
