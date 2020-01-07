import time
from common.scene import Scene
from common.tool import load_resource
from azurelane.assist import calculate_move_map


def difficult_small(prefix):
    return Scene('检测中型舰队标志',
                 identify_image=load_resource("difficult_medium.png", prefix),
                 tap_offset_x=40, tap_offset_y=30, threshold=0.7)


def difficult_medium(prefix):
    return Scene('检测中型舰队标志',
                 identify_image=load_resource("difficult_medium.png", prefix),
                 tap_offset_x=40, tap_offset_y=30, threshold=0.7)


def difficult_large(prefix):
    return Scene('检测中型舰队标志',
                 identify_image=load_resource("difficult_medium.png", prefix),
                 tap_offset_x=40, tap_offset_y=30, threshold=0.7)


def map_move_spec_question_mark(prefix):
    return Scene('检测问号探索点',
                 identify_image=load_resource("explore_map_question_mark.png", prefix),
                 tap_offset_y=50)


def load_target_ship_features(prefix):
    return [
        Scene("检测旗舰", identify_image=load_resource("boss_icon_detection2.png", prefix), threshold=0.7),
        Scene("检测旗舰（带人物）", identify_image=load_resource("boss_small.png", prefix), threshold=0.7),
        Scene("检测侦查舰队", identify_image=load_resource("map_ship_type_1.png", prefix)),  # 判断
        Scene("检测航母舰队", identify_image=load_resource("map_ship_type_2.png", prefix)),  # 判断航母舰队
        Scene("检测主力舰队", identify_image=load_resource("map_ship_type_3.png", prefix)),  # 判断主力舰队
        Scene("检测运输舰队", identify_image=load_resource("map_ship_type_4.png", prefix)),  # 判断侦查舰队
        Scene("检测舰队等级", identify_image=load_resource("enemy_level.png", prefix), threshold=0.6, tap_offset_y=-55),
        difficult_small(prefix),   # 小型舰队
        difficult_medium(prefix),  # 中型舰队
        difficult_large(prefix),   # 大型舰队
        map_move_spec_question_mark(prefix)
    ]


class EnemySearch(Scene):
    variables = None
    ship_features = []
    red_zones = [
        ((0, 0), (108, 640)),
        ((108, 0), (1062, 53)),
        ((108, 53), (506, 96)),
        ((108, 96), (303, 141)),
        ((1062, 0), (1136, 65)),
        ((1090, 88), (1136, 195)),
        ((1046, 358), (1136, 472)),
        ((580, 557), (1136, 640)),
    ]

    def __init__(self, name, identify_image, variables):
        super().__init__(name, identify_image)
        self.ship_features = load_target_ship_features('azurelane/assets/search_ship_feature/')
        self.variables = variables

    def before_action(self, _, screen):
        matched = None
        for i in range(len(self.ship_features)):
            feature = self.ship_features[i]
            if feature.matched_in(screen):
                matched = feature
                break
        if matched is not None:
            x, y = matched.where_to_tap(screen)
            if self.__check_in_red_zone(x, y):
                self.type = 'swipe'
            else:
                self.type = 'tap'
                self.tap_x = x
                self.tap_y = y
        else:
            self.type = 'swipe'

    def after_action(self, device, screen):
        if self.type == 'tap':
            # 点击后，预留10s的时间，等待舰队移动到目标点，
            # 避免到达目标点前截图，载入队伍阵型界面时触发了手势滑动操作，改变阵型
            time.sleep(10)

    def how_to_swipe(self):
        return calculate_move_map(self.variables)

    def __check_in_red_zone(self, tap_x, tap_y):
        for i in range(len(self.red_zones)):
            zone = self.red_zones[i]
            rect_left_top = zone[0]
            rect_right_bottom = zone[1]
            if rect_left_top[0] <= tap_x <= rect_right_bottom[0] and rect_left_top[1] <= tap_y <= rect_right_bottom[1]:
                return True
        return False
