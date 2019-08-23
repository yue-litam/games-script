# -*- coding: utf-8 -*-
import cv2
import os
import random
import sys
import time
from PIL import Image

if sys.version_info.major != 3:
    print('请使用python3.x版本')
    exit(1)

image_path = 'resource/image/'


if __name__ == '__main__':
    target = cv2.imread(image_path + 'array.jpg')
    tmp = cv2.imread(image_path + 'attack.png')
    h, w = tmp.shape[:2]
    result = cv2.matchTemplate(target, tmp, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    strmin_val = str(min_val)
    print("匹配率：" + strmin_val)
    cv2.rectangle(target, min_loc, (min_loc[0] + w, min_loc[1] + h), (0, 0, 255))
    cv2.imshow("match", target)
    cv2.waitKey()
    cv2.destroyAllWindows()
