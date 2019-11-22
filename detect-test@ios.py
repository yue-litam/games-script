import numpy as np
import cv2
import wda


def main():
    image_path = './temp/screen.png'
    feature_path = './arknights/assets/640x1136/feature/level_info_detection.png'

    c = wda.Client()
    _ = c.screenshot(image_path)
    screen = cv2.imread(image_path)  # 加载图片
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # 灰度转换
    # screen_gray = cv2.imread(image_path, 0)

    feature = cv2.imread(feature_path, 0)
    feature_w, feature_h = feature.shape[::-1]
    print('feature size:', feature_w, 'x', feature_h)

    res = cv2.matchTemplate(screen_gray, feature, cv2.TM_CCOEFF_NORMED)

    # 使用灰度图像中的坐标对原始RGB图像进行标记
    loc = np.where(res >= 0.6)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + feature_w, pt[1] + feature_h), (7, 249, 151), 2)

    # 显示图像
    cv2.imshow('Detected', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
