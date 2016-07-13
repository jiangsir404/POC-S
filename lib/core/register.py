#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import types
import sys
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.exception import RegisterDataException, RegisterMutexException, RegisterValueException


class Register:
    def __init__(self, mutex=False, mutex_errmsg=None):
        self.targets = []
        self.mutex = True if mutex else False
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
        self.__verified_check()
        self.__mutex_check()

    def __mutex_check(self):
        if self.mutex and len(self.verified) > 1:
            if self.mutex_errmsg is None:
                raise RegisterMutexException('conflicted functions count: ' + str(len(self.verified)))
            else:
                sys.exit(logger.log(CUSTOM_LOGGING.ERROR, self.mutex_errmsg))

    def __input_vector_check(self):
        if len(self.targets) is 0:
            msg = 'no target'
            raise RegisterDataException(msg)

    def __verified_check(self):
        if len(self.verified) is 0:
            msg = 'no verified target'
            raise RegisterDataException(msg)
