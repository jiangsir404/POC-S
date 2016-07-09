#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import os


# TODO 这里改成统一的path调用？
def initial():
    currentUserHomePath = os.path.expanduser('~')
    _ = """[zoomeye]\nusername = Your ZoomEye Username\npassword = Your ZoomEye Password\n\n[token]\nseebug = Your Seebug Token"""
    if not os.path.isfile(currentUserHomePath + '/.rc'):
        with open(os.path.join(currentUserHomePath, '.rc'), 'w') as fp:
            fp.write(_)


initial()
