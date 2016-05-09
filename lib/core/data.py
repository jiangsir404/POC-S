# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

from lib.core.log import LOGGER
# object to share within function and classes command
# line options and settings
"""
paths
    ROOT_PATH
    DATA_PATH
    MODULES_PATH
    OUTPUT_PATH
    UA_LIST_PATH
    WEAK_PASS
    LARGE_WEAK_PASS

conf
    MODULE_NAME        **
    MODULE_FILE_PATH   **.py
    MODULE_MODE        f / i / n
    INPUT_FILE_PATH    path
    SCREEN_OUTPUT      T / F
    FILE_OUTPUT        T / F
    OUTPUT_FILE_PATH   path
    THREADS_NUM        int
    I_NUM2             string
    SINGLE_MODE        T / F
    ENGINE             t / c
    DEBUG              T / F
    UPDATE             T / F
    NETWORK_STR        string
    RANDOM_UA          T / F
    # TODO
    DISABLE_COLOR      T / F

th
    queue
    THREADS_NUM
    UA_LIST

"""

logger = LOGGER


conf = {}

paths = {}

th = {}

