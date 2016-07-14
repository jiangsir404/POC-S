#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
互斥控制类 用于注册互斥的参数并给出错误提示

Register()
 start         最少通过量
 stop          最大通过量
 mutex         互斥开关
 mutex_errmsg  错误提示

add()
 perform       目标函数
 trigger       触发条件
 args          参数传入
 kwargs        参数传入

Usage:
 r = Register()
 r.add(function1,1>1)
 r.add(function2,2>1)
 r.add(function3,3>1)
 r.run()

"""

import types
import sys
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.exception import RegisterDataException, RegisterMutexException, RegisterValueException


class Register:
    def __init__(self, start=1, stop=1, mutex_errmsg=None, mutex=True):
        self.targets = []
        self.mutex = mutex
        self.start = start
        self.stop = stop
        self.mutex_errmsg = mutex_errmsg
        self.verified = []

    def enable_mutex(self):
        self.mutex = True

    def set_mutex_errmsg(self, s):
        self.mutex_errmsg = str(s)

    def add(self, perform, trigger, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        d = {'perform': perform, 'args': args, 'kwargs': kwargs, 'trigger': trigger}
        self.targets.append(d)
        self.__args = args
        self.__kwargs = kwargs

    def run(self):
        self.__pretreat()
        for target in self.verified:
            if not target.get('perform'):
                msg = 'xxx has no target'
                raise RegisterDataException(msg)
            target.get('perform')(*target.get('args'), **target.get('kwargs'))

    def __pretreat(self):
        self.__input_vector_check()
        for __target in self.targets:
            __trigger = __target.get('trigger')
            if type(__trigger) is types.BooleanType or type(__trigger) is types.StringType:
                if __trigger:
                    self.verified.append(__target)
            else:
                msg = '[Trigger Type Error] Expected:boolean,found:' + str(type(__trigger))
                raise RegisterValueException(msg)
        self.__mutex_check()

    def __mutex_check(self):
        if self.mutex:
            if len(self.verified) < self.start or len(self.verified) > self.stop:
                if self.mutex_errmsg is None:
                    raise RegisterMutexException('mutex error,verified func count: ' + str(len(self.verified)))
                else:
                    sys.exit(logger.log(CUSTOM_LOGGING.ERROR, self.mutex_errmsg))

    def __input_vector_check(self):
        if type(self.stop) is types.IntType and type(self.start) is types.IntType and type(
                self.mutex) is types.BooleanType:
            pass
        else:
            raise RegisterValueException('Register init func type error')
        if len(self.targets) is 0:
            msg = 'no target'
            raise RegisterDataException(msg)
        if self.start > self.stop:
            msg = 'start > stop'
            raise RegisterDataException(msg)
