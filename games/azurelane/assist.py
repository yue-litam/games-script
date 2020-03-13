from common.logutil import logger


def calculate_move_map(context, config):
    width, height = context.screen_width, context.screen_height
    center_x, center_y = width / 2, height / 2  # 屏幕中心坐标
    horizontal_unit_distance = width / 3  # 水平方向每次移动距离
    vertical_unit_distance = height / 3  # 垂直方向每次移动距离
    direction = context.swipe_mode
    opposite_direction = (config.default_swipe_direction + 2) % 4  # 与初始方向相反的方向值
    if direction == 0:
        logger.debug('↑')  # 手势从上往下，查看上侧区域
        to_x = center_x
        to_y = center_y + vertical_unit_distance
        if opposite_direction == direction or opposite_direction + 1 == direction:
            to_y += vertical_unit_distance
        context.swipe_mode = 1  # 下次向右滑动
    elif direction == 1:
        logger.debug('→')  # 手势从右往左，查看右侧区域
        to_x = center_x - horizontal_unit_distance
        if opposite_direction == direction or opposite_direction + 1 == direction:
            to_x -= horizontal_unit_distance
        to_y = center_y
        context.swipe_mode = 2  # 下次向下滑动
    elif direction == 2:
        logger.debug('↓')  # 手势从下往上，查看下侧区域
        to_x = center_x
        to_y = center_y - vertical_unit_distance
        if opposite_direction == direction or opposite_direction + 1 == direction:
            to_y -= vertical_unit_distance
        context.swipe_mode = 3  # 下次向左滑动
    elif direction == 3:
        logger.debug('←')  # 手势从左往右，查看左侧区域
        to_x = center_x + horizontal_unit_distance
        if opposite_direction == direction or opposite_direction + 1 == direction:
            to_x += horizontal_unit_distance
        to_y = center_y
        context.swipe_mode = 0  # 下次向上滑动
    else:
        raise ValueError('移动方向值不存在:%s' % direction)
    return center_x, center_y, to_x, to_y
