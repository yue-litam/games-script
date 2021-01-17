from common.logutil import logger


def calculate_move_map(context, _):
    width, height = context.screen_width, context.screen_height
    center_x, center_y = width / 2, height / 2  # 屏幕中心坐标
    horizontal_unit_distance = width / 3.5  # 水平方向每次移动距离
    vertical_unit_distance = height / 4  # 垂直方向每次移动距离

    if context.swipe_hor_positive:
        if context.swipe_hor_times < 2:
            context.swipe_hor_times += 1
            to_x = center_x - horizontal_unit_distance
            to_y = center_y
        else:
            context.swipe_hor_positive = False
            to_x = center_x
            if context.swipe_ver_positive:
                if context.swipe_ver_times < 2:
                    context.swipe_ver_times += 1
                    to_y = center_y + vertical_unit_distance
                else:
                    context.swipe_ver_positive = False
                    context.swipe_ver_times -= 1
                    to_y = center_y - vertical_unit_distance
            else:
                if context.swipe_ver_times > -2:
                    context.swipe_ver_times -= 1
                    to_y = center_y - vertical_unit_distance
                else:
                    context.swipe_ver_positive = True
                    context.swipe_ver_times += 1
                    to_y = center_y + vertical_unit_distance
    else:
        to_y = center_y
        if context.swipe_hor_times > -2:
            context.swipe_hor_times -= 1
            to_x = center_x + horizontal_unit_distance
        else:
            context.swipe_hor_positive = True
            to_x = center_x
            if context.swipe_ver_positive:
                if context.swipe_ver_times < 2:
                    context.swipe_ver_times += 1
                    to_y = center_y + vertical_unit_distance
                else:
                    context.swipe_ver_positive = False
                    context.swipe_ver_times -= 1
                    to_y = center_y - vertical_unit_distance
            else:
                if context.swipe_ver_times > -2:
                    context.swipe_ver_times -= 1
                    to_y = center_y - vertical_unit_distance
                else:
                    context.swipe_ver_positive = True
                    context.swipe_ver_times += 1
                    to_y = center_y + vertical_unit_distance
    return center_x, center_y, to_x, to_y
