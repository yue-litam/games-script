# -*- coding: utf-8 -*-
import os
import subprocess
import platform
from common.logutil import logger


class Adb:
    def __init__(self, adb_path='adb', device=''):
        try:
            # adb_path = 'adb'
            subprocess.Popen([adb_path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            self.adb_path = adb_path
            if device == '':
                self.device = ''
            else:
                self.device = ' -s ' + device + ' '
        except OSError:
            if platform.system() == 'Windows':
                adb_path = os.path.join('Tools', "adb", 'adb.exe')
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.adb_path = adb_path
                except OSError:
                    pass
            else:
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except OSError:
                    pass
            logger.warn('请安装 ADB 及驱动并配置环境变量')
            exit(1)

    def get_screen(self, d=''):
        command = self.adb_command(d, 'shell wm size')
        process = os.popen(command)
        output = process.read()
        return output

    def get_size(self, d=''):
        output = self.get_screen(d)
        output = output.split(':')[1][1:]
        output = output.split('x')
        return int(output[0]), int(output[1])

    def run(self, raw_command, d=''):
        command = self.adb_command(d, raw_command)
        process = os.popen(command)
        output = process.read()
        return output

    def test_device(self):
        logger.info('检查设备是否连接...')
        command_list = [self.adb_path, 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        device_list = output[0].decode('utf-8')\
            .replace('\r', '')\
            .strip('\n')\
            .split("\n")
        if len(device_list) == 1:  # first one is: 'List of devices attached'
            logger.warn('未找到设备')
            exit(1)
        logger.info('设备已连接')
        logger.info('adb 输出:')
        for i in range(1, len(device_list)):
            if device_list[i] != '':
                logger.info('\t' + device_list[i])

    def test_density(self, d=''):
        command = self.adb_command(d, 'shell wm density')
        process = os.popen(command)
        output = process.read()
        return output

    def test_device_detail(self, d=''):
        command = self.adb_command(d, 'shell getprop ro.product.device')
        process = os.popen(command)
        output = process.read()
        return output

    def test_device_os(self, d=''):
        command = self.adb_command(d, 'shell getprop ro.build.version.release')
        process = os.popen(command)
        output = process.read()
        return output

    def adb_path(self):
        return self.adb_path

    def adb_command(self, device='', command=''):
        return '{0} {1} {2}'.format(
            self.adb_path,
            (self.device if device == '' else (' -s ' + device + ' ')),
            command)
