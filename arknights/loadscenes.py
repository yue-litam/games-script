import sys
sys.path.insert(1, '../common')
from common.scene import Scene


def account_upgrade_detection(device=None, prefix=''):
    return Scene('account_upgrade_detection.png',
                 device.execute_tap_action if device is not None else None,
                 None,
                 prefix)


def prts_disable_detection(device=None, prefix=''):
    return Scene('prts_disable_detection.png',
                 device.execute_tap_action if device is not None else None,
                 None,
                 prefix)


def level_info_detection(device=None, prefix=''):
    def touch_offset(template, screen):
        w, h = template.shape[::-1]
        if device is not None:
            device.execute_tap_action(template, screen, w)

    return Scene('level_info_detection.png', touch_offset, None, prefix)


def prts_running_scene(_, prefix=''):
    def touch_nothing(_1, _2):
        print('.', sep='', end='')
        pass

    return Scene('level_fighting_detection.png', touch_nothing, None, prefix)


def level_team_detection(device=None, prefix=''):
    if device.runtime is None:
        raise Exception('runtime config is None')

    def touch(template, img):
        device.runtime.round_count += 1
        print('\n第 %03d 次副本' % device.runtime.round_count, sep='', end='')
        if device is not None:
            device.execute_tap_action(template, img)

    return Scene('level_team_detection.png', touch, None, prefix)


def level_finish_detection(device=None, prefix=''):
    def touch(template, img):
        if device is not None:
            device.execute_tap_action(template, img)

    return Scene('level_finish_detection.png', touch, None, prefix)


def exchange_intellect_by_pharmacy(device=None, prefix=''):
    if device.runtime is None:
        raise Exception('runtime config is None')

    def touch(template, img):
        if device.runtime.use_pharmacy_auto:
            if device.runtime.used_pharmacy_count >= device.runtime.use_pharmacy_max:
                print('\n已到达预设的可用理智上限, 脚本将退出')
                exit(0)
            else:
                device.runtime.used_pharmacy_count += 1
                if device is not None:
                    device.execute_tap_action(template, img)
        else:
            print('理智不足，自动退出脚本')
            exit(0)

    return Scene('exchange_intellect_by_pharmacy.png', touch,
                 "exchange_intellect_confirm.png", prefix)


def exchange_intellect_by_stone(device=None, prefix=''):
    if device.runtime is None:
        raise Exception('runtime config is None')

    def touch(template, img):
        if device.runtime.use_stone_auto:
            if device.runtime.used_stone_count >= device.runtime.use_stone_max:
                print('\n已到达预设的可用理智上限, 脚本将退出')
                exit(0)
            else:
                device.runtime.used_stone_count += 1
                if device is not None:
                    device.execute_tap_action(template, img)
        else:
            print('理智不足，自动退出脚本')
            exit(0)

    return Scene('exchange_intellect_by_stone.png', touch,
                 "exchange_intellect_confirm.png", prefix)
