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

    # # 查看三组图像(图像标签名称，文件名称)
    # cv2.imshow('screen', screen)
    # cv2.imshow('screen_gray', screen_gray)
    # cv2.imshow('feature', feature)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    res = cv2.matchTemplate(screen_gray, feature, cv2.TM_CCOEFF_NORMED)

    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # touch_loc = (max_loc[0], max_loc[1])
    # cv2.rectangle(screen, touch_loc, (touch_loc[0] + feature_w, touch_loc[1] + feature_h), (7, 249, 151), 2)

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
