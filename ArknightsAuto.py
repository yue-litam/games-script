# -*- coding: utf-8 -*-
import cv2
import os
import random
import sys
import time
from PIL import Image
import Moving
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)
try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

adb = auto_adb()
adb.test_device()


def tap_scale(pos, scale):
    scaled_pos = int(pos[0] * scale[0]), int(pos[1] * scale[1])
    adb.run('shell input tap {} {}'.format(scaled_pos[0], scaled_pos[1]))
    return scaled_pos


def main():
    loop = 0
    screenshot.check_screenshot()
    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)
    x, y = adb.get_size()
    if x < y:
        x, y = y, x
    scale = (x / 960, y / 540)

    pos, val = Moving.find_stage(im, 'go')
    tap_scale(pos, scale)
    time.sleep(3)

    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)
    pos, val = Moving.go(im)
    tap_scale(pos, scale)

    while True:
        loop += 1
        print('开始第', loop, '次战斗')

        time.sleep(90)
        val = 1
        while val > 0.06:
            time.sleep(2)
            print("判断是否战斗结束")
            # 获取作战结果
            im = screenshot.pull_screenshot()
            im = screenshot.Image2OpenCV(im)
            pos, val = Moving.finish(im)

        # 返回关卡界面
        tap_scale((900, 100), scale)
        time.sleep(10)

        im = screenshot.pull_screenshot()
        im = screenshot.Image2OpenCV(im)
        pos, val = Moving.find_stage(im, 'go')
        tap_scale(pos, scale)
        time.sleep(3)

        # 检查理智值是否不足
        im = screenshot.pull_screenshot()
        im = screenshot.Image2OpenCV(im)
        print("检查理智值")
        pos, val = Moving.outofmind(im)
        if val < 0.1:
            print("理智值不足，退出脚本")
            break
        else:
            im = screenshot.pull_screenshot()
            im = screenshot.Image2OpenCV(im)
            pos, val = Moving.go(im)
            tap_scale(pos, scale)


if __name__ == '__main__':
    main()
