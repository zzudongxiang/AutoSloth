#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from datetime import datetime
import time
import sys
import cv2
import os


import libutils.asp_log as log
from libutils.asp_system import clear_all
from interface.ets2_vision import Vision
from interface.ets2_speed import Speed

V = Vision({'fps': 15})
_Speed = Speed({})
def show(image):
    cv2.imshow('image_2', image)
    cv2.waitKey(1)

V.registerd_source('Euro Truck Simulator 2')
V.registered_hook(_Speed.source)
V.registered_hook(show)
time.sleep(30)
V.stop_all()
clear_all()