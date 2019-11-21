import cv2
import numpy as np
from arknights.android import AndroidEventLoop

screen_path = 'temp/screen.png'


def main():
    device = AndroidEventLoop()
    screen = np.asarray(device.pull_screenshot())  # 加载图片
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)  # 灰度转换

    feature_path = './arknights/assets/640x1136/feature/level_team_detection.png'
    feature = cv2.imread(feature_path, 0)
    feature_w, feature_h = feature.shape[::-1]
    print('feature size:', feature_w, 'x', feature_h)

    res = cv2.matchTemplate(screen_gray, feature, cv2.TM_CCOEFF_NORMED)

    # 使用灰度图像中的坐标对原始RGB图像进行标记
    loc = np.where(res >= 0.8)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + feature_w, pt[1] + feature_h), (7, 249, 151), 2)

    # 显示图像
    cv2.imshow('Detected', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
