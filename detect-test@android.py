import cv2
import numpy as np
import sys
import os
import subprocess

from io import StringIO
from PIL import ImageFile, Image

ImageFile.LOAD_TRUNCATED_IMAGES = True
screen_path = 'temp/arknights.png'

try:
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

# SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
SCREENSHOT_WAY = 3
adb = auto_adb(device='127.0.0.1:7555')
adb.test_device()
screen_path = 'temp/screen.png'


def main():
    feature_path = './assets/640x1136/feature/exchange_intellect_confirm.png'

    x, y = adb.get_size()
    print("ScreenWidth: {0}, ScreenHeight: {1}".format(x, y))
    check_screenshot()

    screen = np.asarray(pull_screenshot())  # 加载图片
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)  # 灰度转换

    feature = cv2.imread(feature_path, 0)
    feature_w, feature_h = feature.shape[::-1]
    print('feature size:', feature_w, 'x', feature_h)

    res = cv2.matchTemplate(screen_gray, feature, cv2.TM_SQDIFF_NORMED)

    # 使用灰度图像中的坐标对原始RGB图像进行标记
    loc = np.where(res >= 0.8)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + feature_w, pt[1] + feature_h), (7, 249, 151), 2)

    # 显示图像
    cv2.imshow('Detected', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def check_screenshot():
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
        im = pull_screenshot()
        im.load()
        im.close()
        print('采用方式 {} 获取截图'.format(SCREENSHOT_WAY))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot()


def pull_screenshot():
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
        adb.run('shell screencap -p /sdcard/screen.png')
        adb.run('pull /sdcard/screen.png ./temp/')
        return Image.open('./temp/screen.png')


if __name__ == '__main__':
    main()
