#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from datetime import datetime
import sys
import os
if __name__ == '__main__':
    sys_path = os.path.join(os.path.dirname(__file__), '../')
    sys_path = os.path.abspath(sys_path)
    sys.path.append(sys_path)

from utils.lib_config import init_param

import cv2
class Speed:

    def __init__(self, param):
        self.pid_p = 1
        self.pid_i = 1
        self.pid_d = 1
        init_param(self, param)
        self.target = 0

    def get_real(self):
        return 0

    def get_target(self):
        return self.target

    def source(self, image):
        cv2.imshow('image', image)
        cv2.waitKey(1)

    def set_target(self, target):
        self.target = target

    def stop(self):
        self.set_target(0)

    def get_history(self):
        return self.history

    def clear_history(self):
        self.clear_history = []

    def add_history(self, speed):
        self.clear_history.append([datetime.now(), speed])
