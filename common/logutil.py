#!/usr/bin/python
# -*- encoding:utf-8 -*-
import errno
import logging.config
import os


def mkdir_p(path):
    # see reference:
    # https://stackoverflow.com/questions/28054864/use-fileconfig-to-configure-custom-handlers-in-python
    # https://stackoverflow.com/questions/20666764/python-logging-how-to-ensure-logfile-directory-is-created
    """http://stackoverflow.com/a/600612/190597 (tzot)"""
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


class MakeFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding='utf-8', delay=0):
        mkdir_p(os.path.dirname(filename))
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)


logging.handlers.MakeFileHandler = MakeFileHandler
# see reference: https://www.jianshu.com/p/feb86c06c4f4
logging.config.fileConfig("conf/logging.conf")

# create logger
logger = logging.getLogger()


# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')
