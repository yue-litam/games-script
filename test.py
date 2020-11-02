import cv2
import numpy as np

from common.device.c_android import AndroidDevice
from common.device.c_ios import IOSDevice
from common.runtime import Config
from games.azurelane.scenes.enemy_search import EnemySearch


def main():
    # 从设备获得屏幕截图
    cfg = Config()
    # cfg.device_type = 'local'
    print(cfg)
    width = 1136
    height = 640

    if cfg.device_type == 'ios':
        d = IOSDevice(cfg=cfg)
        width = d.screen_x
        height = d.screen_y
        screen = d.screen_capture_handler(gray=False)
    elif cfg.device_type == 'android':
        d = AndroidDevice(cfg=cfg)
        width = d.screen_x
        height = d.screen_y
        screen = d.screen_capture_handler(gray=False)
    else:
        # 读取本地磁盘的截屏文件
        screen = cv2.imread(cfg.screenshot_to_disk_file_name)

    # 灰度转换方法一: 读取RGB后转换
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    # 灰度转换方法二: 直接读取
    # screen_gray = cv2.imread(image_path, 0)

    feature_paths = [
        # ('./games/azurelane/assets/search_ship_feature/map_ship_type_1.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/map_ship_type_2.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/map_ship_type_3.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/map_ship_type_3_.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/map_ship_type_4.png', 0.8),
        # ('./games/azurelane/assets/search_ship_feature/enemy_level.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/difficult_medium.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/map_ship_typeb_3.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/boss_icon_detection.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/boss_icon_detection2.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/boss_small.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/boss_small2.png', 0.7),
        # ('./games/azurelane/assets/search_ship_feature/explore_map_question_mark.png', 0.7),
        # ('./games/azurelane/assets/scenes_feature/jp/choose_level_go_now_button.png', 0.7),
    ]
    for fp in feature_paths:
        feature = cv2.imread(fp[0], 0)
        feature_w, feature_h = feature.shape[::-1]
        res = cv2.matchTemplate(screen_gray, feature, cv2.TM_CCOEFF_NORMED)
        print(fp[0])
        possible_targets = []
        # 使用灰度图像中的坐标对原始RGB图像进行标记
        loc = np.where(res >= fp[1])
        for pt in zip(*loc[::-1]):
            x, y = pt[0] + feature_w / 2, pt[1] + feature_h / 2
            if len(possible_targets) > 0:
                last = possible_targets[len(possible_targets) - 1]
                if x - last[0] > 20:
                    possible_targets.append((x, y))
            else:
                possible_targets.append((x, y))

            cv2.rectangle(screen, pt, (pt[0] + feature_w, pt[1] + feature_h), (7, 249, 151), 2)
        print(possible_targets)

    # 红色方框框出不可点击区域
    if cfg.game_name == 'azurelane':
        red_zones = EnemySearch.red_zones
        for i in range(len(red_zones)):
            zone = red_zones[i]
            cv2.rectangle(screen, zone[0], zone[1], (0, 0, 255), 3)

    # 显示图像
    window_name = "detect-result"
    cv2.namedWindow(window_name, 0)
    cv2.resizeWindow(window_name, width, height)
    cv2.moveWindow(window_name, 100, 100)
    cv2.imshow(window_name, screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
