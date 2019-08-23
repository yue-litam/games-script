# -*- coding: utf-8 -*-
import cv2


def template_matching(screenshot, template):
    image_path = 'resource/image/'
    mid_air = cv2.imread(image_path + template)
    h, w = mid_air.shape[:2]
    result = cv2.matchTemplate(screenshot, mid_air, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    strmin_val = str(min_val)
    print("匹配度：" + strmin_val)
    # cv2.rectangle(screenshot, min_loc, (min_loc[0] + w, min_loc[1] + h), (0, 0, 255))
    pos = (min_loc[0] + w / 2, min_loc[1] + h / 2)

    # cv2.imshow("match", screenshot)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return pos, min_val


def find_stage(screenshot, stage):
    pos, val = template_matching(screenshot, stage + '.png')
    pos = (pos[0], pos[1])
    return pos, val


def go(screenshot):
    return template_matching(screenshot, 'go2.png')


def finish(screenshot):
    return template_matching(screenshot, 'opsend.png')


def outofmind(screenshot):
    return template_matching(screenshot, 'outofmind.png')