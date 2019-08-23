# -*- coding: utf-8 -*-
"""
手机屏幕截图的代码
"""
import subprocess
import os
import sys
import cv2
import numpy
from PIL import Image
from io import StringIO

try:
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)
adb = auto_adb()
# SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
SCREENSHOT_WAY = 3


def pull_screenshot():
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序
    """
    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            adb.adb_path + ' shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        return Image.open(StringIO(binary_screenshot))
    elif SCREENSHOT_WAY == 0:
        adb.run('shell screencap -p /sdcard/arknights.jpg')
        adb.run('pull /sdcard/arknights.jpg .')
        return Image.open('./arknights.jpg').resize((960, 540))


def check_screenshot():
    """
    检查获取截图的方式
    """
    global SCREENSHOT_WAY
    SCREENSHOT_WAY = 0
    if os.path.isfile('arknights.jpg'):
        try:
            os.remove('arknights.jpg')
        except Exception:
            pass
    if SCREENSHOT_WAY < 0:
        print('暂不支持当前设备')
        sys.exit()
    try:
        im = pull_screenshot()
        im.load()
        im.close()
        print('采用方式 {} 获取截图'.format(SCREENSHOT_WAY))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot()


def Image2OpenCV(im):
    return cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)


def OpenCV2Image(cv):
    return Image.fromarray(cv2.cvtColor(cv, cv2.COLOR_BGR2RGB))
