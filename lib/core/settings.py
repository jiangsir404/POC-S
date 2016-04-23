# !/usr/bin/env python
#  -*- coding: utf-8 -*-

__author__ = 'xy'

import os
import subprocess

VERSION = '1.3'
VERSION_STRING = "POC-T"
AUTHOR = 'cdxy'
MAIL = 'i@cdxy.me'
PLATFORM = os.name

IS_WIN = subprocess.mswindows

# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"

ISSUES_PAGE = "https://github.com/Xyntax/POC-T/issues"
GIT_REPOSITORY = "git@github.com:Xyntax/POC-T.git"
GIT_PAGE = "https://github.com/Xyntax/POC-T"

BANNER = """\033[01;34m
                                             \033[01;31m__/\033[01;34m
    ____     ____     _____           ______\033[01;33m/ \033[01;31m__/\033[01;34m
   / __ \   / __ \   / ___/   ____   /__  __/\033[01;33m_/\033[01;34m
  / /_/ /  / /_/ /  / /___   /___/     / /
 / /___/   \____/   \____/            / /
/_/                                  /_/
    \033[01;37m{\033[01;m Version %s by %s mail:%s \033[01;37m}\033[0m
""" % (VERSION, AUTHOR, MAIL)

# print BANNER
