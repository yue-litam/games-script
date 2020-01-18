import numpy as np
import cv2
import wda
from common.logutil import logger
from azurelane.scenes.enemy_search import EnemySearch


def main():
    image_path = './temp/screen.png'
    feature_path = './azurelane/assets/scenes_feature/fallback_and_switch_btn.png'

    c = wda.Client()
    _ = c.screenshot(image_path)
    screen = cv2.imread(image_path)  # 加载图片
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # 灰度转换
    # screen_gray = cv2.imread(image_path, 0)

    feature = cv2.imread(feature_path, 0)
    feature_w, feature_h = feature.shape[::-1]
    logger.info('feature size: {0}x{1}'.format(feature_w, feature_h))

    res = cv2.matchTemplate(screen_gray, feature, cv2.TM_CCOEFF_NORMED)

    # 使用灰度图像中的坐标对原始RGB图像进行标记
    loc = np.where(res >= 0.6)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + feature_w, pt[1] + feature_h), (7, 249, 151), 2)

    # 红色方框框出不可点击区域
    red_zones = EnemySearch.red_zones
    for i in range(len(red_zones)):
        zone = red_zones[i]
        cv2.rectangle(screen, zone[0], zone[1], (0, 0, 255), 3)

    # 显示图像
    cv2.imshow('Detected', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
