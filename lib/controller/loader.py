# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

from lib.core.data import th, conf
import Queue


def load_payloads():
    # self._print_message("[*] Loading payloads ...")
    th['queue'] = Queue.Queue()
    if conf['MODULE_MODE'] is 'i':
        _int = conf['I_NUM2'].strip().split('-')
        for each in range(int(_int[0].strip()), int(_int[1].strip())):
            th['queue'].put(str(each))

    elif conf['MODULE_MODE'] is 'f':
        with open(conf['INPUT_FILE_PATH']) as f:
            for line in f:
                sub = line.strip()
                if sub:
                    th['queue'].put(sub)
    else:
        raise Exception('conf[\'MODULE_MODE\'] value ERROR.')


