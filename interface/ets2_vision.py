#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from datetime import datetime
import threading
import time
import sys
import os
if __name__ == '__main__':
    sys_path = os.path.join(os.path.dirname(__file__), '../')
    sys_path = os.path.abspath(sys_path)
    sys.path.append(sys_path)

import libutils.asp_log as log
from libutils.asp_config import init_param
from libutils.asp_windows import grab_windows


class Vision:

    def __init__(self, param):
        self.fps = 30
        init_param(self, param)
        self.hooks = {}

    def __thread_loop(self, get_frame, hook):
        total_sleep = 1 / self.fps
        hook_name = str(hook)
        while self.hooks[hook_name]:
            self.fps_real = 1
            start_time = datetime.now()
            image = get_frame()
            if image is not None:
                hook(image)
            do_work = (datetime.now() - start_time).total_seconds()
            sleep = total_sleep - do_work if total_sleep - do_work > 0 else 0
            log.V('Thread Loop Sleep %f' % sleep)
            time.sleep(sleep)

    def registerd_source(self, windows_name):
        self.windows_name = windows_name
        log.D('Set Source Windows %s' % self.windows_name)

    def get_frame(self):
        return grab_windows(self.windows_name)

    def registered_hook(self, hook):
        hook_name = str(hook)
        if hook_name not in self.hooks or not self.hooks[hook_name]:
            self.hooks[hook_name] = True
            threading.Thread(target=self.__thread_loop,
                             args=(self.get_frame, hook)).start()
            log.I('Start Hook %s Thread' % hook_name)
        else:
            log.W('Hook in Queue, Dup Registered %s' % hook_name)

    def stop_all(self):
        count = 0
        for hook_name in self.hooks:
            if self.hooks[hook_name]:
                count += 1
            self.hooks[hook_name] = False
        log.W('Stop All(%d) Hook Thread' % count)

    def get_hooks(self):
        return self.hooks
