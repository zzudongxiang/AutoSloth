#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import threading
import time
import json
import sys
import os

sys_path = os.path.join(os.path.dirname(__file__), '../')
sys_path = os.path.abspath(sys_path)
if __name__ == '__main__':
    sys.path.append(sys_path)

__config_path__ = os.path.join(sys_path, 'config.json')
__config_data__ = {}


def load():
    global __config_data__
    if not os.path.exists(__config_path__):
        return
    if os.path.getsize(__config_path__) <= 0:
        return
    with open(__config_path__, 'r+', encoding='utf-8') as file:
        __config_data__ = json.load(file)


def dump():
    with open(__config_path__, 'w+', encoding='utf-8') as file:
        json.dump(__config_data__, file, indent=4)


def get(section, key, default=''):
    if section not in __config_data__:
        __config_data__[section] = {}
    if key not in __config_data__[section]:
        __config_data__[section][key] = default
        dump()
    return __config_data__[section][key]


def init_param(obj, param):
    for key in obj.__dict__:
        if key in param:
            setattr(obj, key, param[key])


load()
