import cv2
import numpy as np
from PIL import Image
from common.device.c_android import AndroidDevice
from azurelane.scenes.enemy_search import EnemySearch
from logutil import logger

screen_path = 'temp/screen.png'


def main():
    device = AndroidDevice()
    screen = np.asarray(device.screen_capture_as_image())  # 实时截取并加载图片
    # screen = np.asarray(Image.open('./temp/screen.png'))  # 加载本地图片
    # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)  # 翻转RGB顺序
    gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)  # 灰度转换

    # feature_path = './azurelane/assets/scenes_feature/safe_lane.png'
    # feature_path = './azurelane/assets/scenes_feature/team_choose.png'
    # feature_path = './azurelane/assets/scenes_feature/fallback_and_switch_btn.png'
    # feature_path = './azurelane/assets/scenes_feature/difficult_medium.png'
    # feature_path = './azurelane/assets/scenes_feature/shipyard_full.png'
    feature_path = './azurelane/assets/scenes_feature/map_ship_type_2.png'
    # feature_path = './azurelane/assets/scenes_feature/enemy_level.png'
    feature = cv2.imread(feature_path, 0)
    feature_w, feature_h = feature.shape[::-1]
    logger.info('scenes_feature size:', feature_w, 'x', feature_h)

    res = cv2.matchTemplate(gray, feature, cv2.TM_CCOEFF_NORMED)

    # 使用灰度图像中的坐标对原始RGB图像进行标记
    loc = np.where(res >= 0.8)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + feature_w, pt[1] + feature_h), (7, 249, 151), 2)

    s = EnemySearch('', None, None)
    red_zones = s.red_zones
    for i in range(len(red_zones)):
        zone = red_zones[i]
        cv2.rectangle(screen, zone[0], zone[1], (0, 0, 255), 3)

    # 显示图像
    cv2.imshow('Detected', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
