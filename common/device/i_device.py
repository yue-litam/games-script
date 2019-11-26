class Device:
    runtime = None

    def __init__(self, runtime=None):
        self.runtime = runtime

    def screen_capture_handler(self, file_name=''):
        raise NotImplementedError("Should have implemented this: 截屏方法")

    def tap_handler(self, pos_x, pos_y):
        raise NotImplementedError("Should have implemented this: 触摸屏幕指令方法")

    def debug(self, message):
        if self.runtime is not None and self.runtime.log_level == 'debug':
            print(message)
