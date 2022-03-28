#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import os
if __name__ == '__main__':
    sys_path = os.path.join(os.path.dirname(__file__), '../')
    sys_path = os.path.abspath(sys_path)
    sys.path.append(sys_path)

import threading

import time

__thread_id__ = 0


class Thread(threading.Thread):

    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.status = True

    def register(self, do_work):
        self.do_work = do_work

    def run(self):
        while self.status:
            print('run', self.name, self.native_id)
            time.sleep(0.5)

    def __del__(self):
        self.status = False
        print('del')


class A:

    def __init__(self):
        self.t = Thread("t1", 3)
        self.t.start()

    def __del__(self):
        del self.t


a = A()
time.sleep(3)
del a
