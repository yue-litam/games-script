# coding: utf-8

import os
import subprocess
import sys
from io import StringIO

import cv2
import numpy
from PIL import ImageFile, Image

from common.device.adb import Adb
from common.device.i_device import Device
from common.logutil import logger
from common.runtime import Config

ImageFile.LOAD_TRUNCATED_IMAGES = True


class AndroidDevice(Device):
    SCREENSHOT_WAY = 3
    adb = None

    def __init__(self, cfg=None, address='127.0.0.1:7555'):
        self.adb = Adb(device=address)
        self.adb.test_device()
        self.__check_screenshot()
        self.screen_x, self.screen_y = self.adb.get_size()
        self.cfg = cfg if cfg is not None else Config()

    def tap_handler(self, pos_x, pos_y):
        logger.debug('actually tap position: {0}, {1}'.format(pos_x, pos_y))
        self.adb.run('shell input tap {} {}'.format(pos_x, pos_y))

    def swipe_handler(self, from_x, from_y, to_x, to_y, millisecond):
        self.adb.run('shell input swipe {} {} {} {} {}'.format(from_x, from_y, to_x, to_y, millisecond))

    def screen_capture_handler(self, gray=True):
        screen = self.__pull_screenshot(self.cfg.screenshot_to_disk_file_name)
        data = numpy.asarray(screen)
        if gray:
            return cv2.cvtColor(data, cv2.COLOR_RGB2GRAY)
        else:
            return data

    def screen_capture_as_image(self):
        return self.__pull_screenshot()

    def __check_screenshot(self):
        while True:
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

    def __pull_screenshot(self, file_name=None):
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

            default_temporary_file_name = './temp/android-screenshot.png'
            if file_name is None:
                file_name = default_temporary_file_name
            self.adb.run('shell screencap -p /sdcard/screenshot.png')

            if os.path.isfile(file_name):
                # noinspection PyBroadException
                try:
                    os.remove(file_name)
                except Exception:
                    pass
            # 从安卓虚拟机复制截图到本机磁盘后打开
            self.adb.run('pull /sdcard/screenshot.png ' + file_name)
            return Image.open(file_name)
