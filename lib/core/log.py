#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import logging
import sys

from lib.core.enums import CUSTOM_LOGGING

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")

LOGGER = logging.getLogger("pocketLog")

LOGGER_HANDLER = None
try:
    from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    disableColor = False

    # TODO disable_color in parser.py
    for argument in sys.argv:
        if "disable-col" in argument:
            disableColor = True
            break

    if disableColor:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    else:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

# there can't be -> if conf.DEBUG:
if "debug" in sys.argv:
    FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
else:
    FORMATTER = logging.Formatter("\r[%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.WARNING)
