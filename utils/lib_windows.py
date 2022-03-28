#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import win32gui, pyautogui, cv2, ctypes
import threading, time, sys, os
import numpy as np
if __name__ == '__main__':
    sys_path = os.path.join(os.path.dirname(__file__), '../')
    sys_path = os.path.abspath(sys_path)
    sys.path.append(sys_path)

import utils.lib_log as log


class __Windows:

    def __init__(self, windows_name):
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        self.windows_name = windows_name
        self.handle = 0
        self.__stop = False
        self.__lock = threading.Lock()
        self.__func = ctypes.windll.dwmapi.DwmGetWindowAttribute
        self.__type = ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS)
        self.__rect = ctypes.wintypes.RECT()
        self.__size = ctypes.sizeof(self.__rect)
        self.__pos = ctypes.byref(self.__rect)
        self.update_handle()
        self.update_position()
        self.__stop = False
        threading.Thread(target=self.__thread_loop).start()
        log.I('Start Windows Position Watching Thread')

    def __thread_loop(self):
        while not self.__stop:
            self.update_position()
            log.V('Windows Position Watching %s' % str(self.get_position()))
            time.sleep(0.5)

    def clear(self):
        self.__stop = True
        log.W('Stop Windows Position Watching Thread')

    def update_handle(self):
        self.handle = win32gui.FindWindow(0, self.windows_name)
        log.D('Update Windows Handle')

    def update_position(self):
        if self.handle == 0:
            self.update_handle()
        else:
            hwnd = ctypes.wintypes.HWND(self.handle)
            self.__func(hwnd, self.__type, self.__pos, self.__size)
        with self.__lock:
            self.__x = self.__rect.left
            self.__y = self.__rect.top
            self.__width = self.__rect.right - self.__x
            self.__height = self.__rect.bottom - self.__rect.top

    def get_position(self):
        with self.__lock:
            x = self.__x
            y = self.__y
            width = self.__width
            height = self.__height
        return [x, y, width, height]

    def grab(self):
        with self.__lock:
            region = [self.__x, self.__y, self.__width, self.__height]
        if region[2] > 0 and region[3] > 0:
            image = pyautogui.screenshot(region=region)
            log.V('Grab Image %s' % str(image))
            return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        else:
            return None


__windows_list__ = {}


def grab_windows(windows_name):
    if windows_name not in __windows_list__:
        __windows_list__[windows_name] = __Windows(windows_name)
    return __windows_list__[windows_name].grab()


def get_windows_position(windows_name):
    if windows_name not in __windows_list__:
        __windows_list__[windows_name] = __Windows(windows_name)
    return __windows_list__[windows_name].get_position()


def clear_all():
    for key in __windows_list__:
        __windows_list__[key].clear()
