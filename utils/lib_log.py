#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from datetime import datetime
import traceback
import sys
import os

sys_path = os.path.join(os.path.dirname(__file__), '../')
sys_path = os.path.abspath(sys_path)
if __name__ == '__main__':
    sys.path.append(sys_path)

from utils.lib_config import get
from utils.lib_regex import get_int

__log_level__ = get_int(get('settings', 'log_level', '1'), 1)
__log_path__ = os.path.join(sys_path, 'log/')


class __Log:
    __log_format__ = '[{datetime}] {level} <{file}> {func}(), {line}:'
    __terminal_color__ = {
        'E': [4, '\033[31m%s\033[0m'],
        'W': [3, '\033[33m%s\033[0m'],
        'I': [2, '\033[34m%s\033[0m'],
        'D': [1, '%s'],
        'V': [0, '\033[32m%s\033[0m'],
    }

    def __init__(self, log_path, log_level):
        log = 'log_%s.log' % datetime.now().strftime('%y%m%d_%H%M%S')
        self.__log_level = log_level
        self.__log_path = os.path.join(log_path, log)
        self.__log_path = os.path.abspath(self.__log_path)
        self.__dir_path = os.path.dirname(self.__log_path)
        if not os.path.exists(self.__dir_path):
            os.makedirs(self.__dir_path)
        self.__log_file = open(self.__log_path, 'a+', encoding='utf-8')

    def __del__(self):
        try:
            self.__log_file.close()
        except Exception as Ex:
            print('close log file error', str(Ex))

    def write(self, msg):
        try:
            if msg is not None:
                self.__log_file.writelines(msg + '\n')
                self.__log_file.flush()
        except Exception as Ex:
            print('write log file error', str(Ex))

    def check(self, level):
        level = level.upper() if level in self.__terminal_color__ else 'D'
        return self.__terminal_color__[level][0] >= self.__log_level, level

    def get_info(self, level):
        ret, level = self.check(level)
        trace = traceback.extract_stack()
        for i in range(len(trace)):
            info = trace[len(trace) - i - 1]
            if info.filename != __file__:
                break
        if ret and 'info' in locals():
            param = {
                'line': str(info.lineno),
                'datetime': str(datetime.now()),
                'level': level,
                'file': os.path.basename(info.filename),
                'func': info.name,
            }
            ret = self.__log_format__
            for key in param:
                ret = ret.replace('{%s}' % key, param[key])
        else:
            ret = None
        return ret

    def format_msg(self, level='D', msg=''):
        ret, level = self.check(level)
        return self.__terminal_color__[level][1] % msg if ret else None


__log__ = __Log(__log_path__, __log_level__)


def __prt(level, msg):
    msg = msg.replace('\r', '')
    for item in msg.split('\n'):
        if item.strip() == '':
            continue
        info = __log__.get_info(level)
        if info is None:
            continue
        __log__.write('%s %s' % (info, item))
        print('%s %s' % (info, __log__.format_msg(level, item)))


def E(msg):
    __prt('E', msg)


def W(msg):
    __prt('W', msg)


def I(msg):
    __prt('I', msg)


def D(msg):
    __prt('D', msg)


def V(msg):
    __prt('V', msg)


def error():
    E('~' * 50)
    E(traceback.format_exc())
    E('~' * 50)
