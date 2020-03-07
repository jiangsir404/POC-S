#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import logging
import sys
import requests
from lib.core.enums import CUSTOM_LOGGING

logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("requests").setLevel(logging.CRITICAL)
requests.packages.urllib3.disable_warnings()

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")

LOGGER = logging.getLogger("TookitLogger")

LOGGER_HANDLER = None
try:
    from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    try:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
    except Exception:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

contentFmt = "%(asctime)s [%(filename)s:%(lineno)d][%(levelname)s]:%(message)s"
datetimeFmt = '%Y-%m-%d %H:%M:%S'
FORMATTER = logging.Formatter(contentFmt, datetimeFmt)
#FORMATTER = logging.Formatter("\r[%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.WARNING)

# 调试log用
MY_LOGGER = LOGGER
LOGGER.success = LOGGER.info

# class MY_LOGGER:
#     @staticmethod
#     def success(msg):
#         return LOGGER.log(CUSTOM_LOGGING.SUCCESS, msg)
#
#     @staticmethod
#     def info(msg):
#         return LOGGER.log(CUSTOM_LOGGING.SYSINFO, msg)
#
#     @staticmethod
#     def warning(msg):
#         return LOGGER.log(CUSTOM_LOGGING.WARNING, msg)
#
#     @staticmethod
#     def error(msg):
#         return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)
