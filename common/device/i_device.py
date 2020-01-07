class Device:
    screen_x = 0
    screen_y = 0

    def screen_capture_handler(self, file_name=''):
        raise NotImplementedError("Should have implemented this: 截屏方法")

    def tap_handler(self, pos_x, pos_y):
        raise NotImplementedError("Should have implemented this: 触摸屏幕指令方法")

    def swipe_handler(self, from_x, from_y, to_x, to_y, millisecond):
        raise NotImplementedError("Should have implemented this: 模拟手势滑动指令方法")
