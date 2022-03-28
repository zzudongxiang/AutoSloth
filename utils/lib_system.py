#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import os
if __name__ == '__main__':
    sys_path = os.path.join(os.path.dirname(__file__), '../')
    sys_path = os.path.abspath(sys_path)
    sys.path.append(sys_path)

from utils.lib_windows import clear_all as windows_clear_all

def clear_all():
    windows_clear_all()