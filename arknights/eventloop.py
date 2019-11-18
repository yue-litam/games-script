# coding: utf-8

import time
from common import tool
from scene import Scene
from configparser import ConfigParser


class EventLoop:
    scenes = []
    round_count = 0
    assets_path_prefix = ''

    use_pharmacy_auto = False
    use_pharmacy_max = 0
    used_pharmacy_count = 0

    use_stone_auto = False
    use_stone_max = 0
    used_stone_count = 0

    def __init__(self, assets_path_prefix):

        cfg = ConfigParser()
        try:
            cfg.read('config.ini')
            self.use_stone_auto = cfg.getboolean('intellect', 'use_stone')
            self.use_stone_max = cfg.getint('intellect', 'use_stone_max')
            self.use_pharmacy_auto = cfg.getboolean('intellect', 'use_pharmacy')
            self.use_pharmacy_max = cfg.getint('intellect', 'use_pharmacy_max')
            print('理智不足时')
            print('\t自动使用药剂:{0}, 最多使用数量:{1}'.
                  format(self.use_pharmacy_auto, self.use_pharmacy_max))
            print('\t自动使用石头:{0}, 最多使用数量:{1}'.
                  format(self.use_stone_auto, self.use_stone_max))
            print('')
        except Exception as ex:
            print(ex)

        def level_info_detection():
            def touch_offset(template, screen):
                w, h = template.shape[::-1]
                self.execute_tap_action(template, screen, w)

            return Scene('level_info_detection.png', touch_offset, None, assets_path_prefix)

        def prts_running_scene():
            def touch_nothing(template, img):
                print('.', sep='', end='')
                pass

            return Scene('level_fighting_detection.png', touch_nothing, None, assets_path_prefix)

        def level_team_detection():
            def touch(template, img):
                self.round_count += 1
                print('\n第 %03d 次副本' % self.round_count, sep='', end='')
                self.execute_tap_action(template, img)

            return Scene('level_team_detection.png', touch, None, assets_path_prefix)

        def level_finish_detection():
            def touch(template, img):
                # TODO 副本结束后获取物资清单
                # print('结束, 获得物资:')
                self.execute_tap_action(template, img)

            return Scene('level_finish_detection.png', touch, None, assets_path_prefix)

        def exchange_intellect_by_pharmacy():
            def touch(template, img):
                if self.use_pharmacy_auto:
                    if self.used_pharmacy_count >= self.use_pharmacy_max:
                        print('\n已到达预设的可用理智上限, 脚本将退出')
                        exit(0)
                    else:
                        self.used_pharmacy_count += 1
                        self.execute_tap_action(template, img)
                else:
                    print('理智不足，自动退出脚本')
                    exit(0)

            return Scene('exchange_intellect_by_pharmacy.png', touch,
                         "exchange_intellect_confirm.png", assets_path_prefix)

        def exchange_intellect_by_stone():
            def touch(template, img):
                if self.use_stone_auto:
                    if self.used_stone_count >= self.use_stone_max:
                        print('\n已到达预设的可用理智上限, 脚本将退出')
                        exit(0)
                    else:
                        self.used_stone_count += 1
                        self.execute_tap_action(template, img)
                else:
                    print('理智不足，自动退出脚本')
                    exit(0)

            return Scene('exchange_intellect_by_stone.png', touch,
                         "exchange_intellect_confirm.png", assets_path_prefix)

        self.scenes = [
            Scene('prts_disable_detection.png', self.execute_tap_action, None, assets_path_prefix),  # 战斗关卡确认出击
            Scene('account_upgrade_detection.png', self.execute_tap_action, None, assets_path_prefix),  # 战斗结束后账号等级提升
            level_info_detection(),  # 战斗关卡确认出击
            level_team_detection(),  # 战斗前队伍预览
            level_finish_detection(),  # 战斗结束后账号等级提升
            prts_running_scene(),  # 副本还在进行中
            exchange_intellect_by_pharmacy(),  # 理智不足时有可使用的药剂
            exchange_intellect_by_stone(),  # 理智不足时有可使用的石头
        ]

    def take_screen_shot_handler(self):
        raise NotImplementedError("Should have implemented this: 截屏方法")

    def device_tap_handler(self, pos_x, pos_y):
        raise NotImplementedError("Should have implemented this: 触摸屏幕指令方法")

    def execute_tap_action(self, template, img, x_offset=0, y_offset=0):
        touch_loc, _, w, h = tool.device_detect_feature_location_handler(template, img)
        x, y = ((touch_loc[0] + w / 2 + x_offset) / 2, (touch_loc[1] + h / 2 + y_offset) / 2)
        # print("Touching {0}, {1}".format(x, y))
        self.device_tap_handler(x, y)

    def recognize_and_process_page(self):
        img = self.take_screen_shot_handler()
        if img is None:
            return

        ss = None
        for scene in self.scenes:
            match = tool.get_similarity(scene.imageTemplate, img, scene) == 1
            if match:
                ss = scene
                break
        if ss is None:
            # print('?', sep='', end='')
            # print('unable recognize scene, wait for next time.')
            return

        scene_name = ss.image_name
        filtered = [s for s in self.scenes if s.image_name == ss.image_name]

        ss = None
        for scene in filtered:
            match = tool.get_similarity(scene.actionTemplate, img, scene) == 1
            if match:
                ss = scene
                break
        if ss is None:
            print('scene', scene_name, ' unable recognize action feature.')
        else:
            # print("Picked : " + ss.image_name + " ==> " + ss.action_button_name)
            ss.action(ss.actionTemplate, img)

    def start(self):
        while True:
            self.recognize_and_process_page()
            time.sleep(1)
