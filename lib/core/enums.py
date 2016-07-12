#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

class CUSTOM_LOGGING:
    SYSINFO = 9
    SUCCESS = 8
    ERROR = 7
    WARNING = 6


class CONTENT_STATUS:
    IN_PROGRESS = 0
    COMPLETE = 1


class EXIT_STATUS:
    SYSETM_EXIT = 0
    ERROR_EXIT = 1
    USER_QUIT = 2


class POC_RESULT_STATUS:
    FAIL = 0
    SUCCESS = 1
    RETRAY = 2


class API_MODE_STATUS:
    ZOOMEYE = 9
    SHODAN = 8


class TARGET_MODE_STATUS:
    FILE = 9
    SINGLE = 8
    IPMASK = 7
    RANGE = 6
    API = 5


class ENGINE_MODE_STATUS:
    THREAD = 9
    GEVENT = 8
