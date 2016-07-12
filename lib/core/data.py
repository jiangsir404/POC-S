#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

from lib.core.log import LOGGER
from lib.core.datatype import AttribDict

"""
paths
    ROOT_PATH
    DATA_PATH
    SCRIPT_PATH
    OUTPUT_PATH
    UA_LIST_PATH
    WEAK_PASS
    LARGE_WEAK_PASS

conf
    MODULE_NAME        **
    MODULE_FILE_PATH   **.py
    TARGET_MODE        f / i / n
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
    OPEN_BROWSER       T / F
    # TODO
    DISABLE_COLOR      T / F

th
    module_obj
    queue
    THREADS_NUM
    UA_LIST
    MODULE_NAME

"""

logger = LOGGER

paths = AttribDict()

cmdLineOptions = AttribDict()

conf = AttribDict()

th = AttribDict()
