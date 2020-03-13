from common.device.c_android import AndroidDevice
from common.device.c_ios import IOSDevice
from common.runtime import Config


def main():
    # 从设备获得屏幕截图
    cfg = Config()
    cfg.screenshot_to_disk = True
    cfg.screenshot_to_disk_file_name = './temp/screenshot.png'
    print(cfg)

    if cfg.device_type == 'ios':
        d = IOSDevice(cfg=cfg)
    elif cfg.device_type == 'android':
        d = AndroidDevice(cfg=cfg)
    else:
        exit(0)
    d.screen_capture_handler()


if __name__ == '__main__':
    main()
