#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import os
import re
if __name__ == '__main__':
    sys_path = os.path.join(os.path.dirname(__file__), '../')
    sys_path = os.path.abspath(sys_path)
    sys.path.append(sys_path)


def __regex(pattern, string, callback=None):
    ret_status = False
    ret_value = string
    if re.match(pattern, string):
        ret_status = True
        ret_value = callback(string) if callback is not None else ret_value
    return ret_status, ret_value


def find_all(pattern, string):
    return re.findall(pattern, string)


def is_float(string):
    return __regex(r'^(\+|\-)?\d+\.?\d*$', string)[0]


def get_float(string, default):
    ret, value = __regex(r'^(\+|\-)?\d+\.?\d*$', string, float)
    return value if ret else default


def is_int(string):
    return __regex(r'^(\+|\-)?\d+$', string)[0]


def get_int(string, default):
    ret, value = __regex(r'^(\+|\-)?\d+$', string, int)
    return value if ret else default