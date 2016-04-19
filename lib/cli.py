# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os.path
from lib.parse.parser import parse_args
from lib.controller.loader import load_payloads
from lib.controller.threads import POC_T
from lib.core.common import setPaths
from lib.core.data import paths, th, conf
from lib.core.settings import DEBUG


def main():
    paths['ROOT_PATH'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    setPaths()
    parse_args()

    print "[*]loading payloads..."
    load_payloads()
    print "total:", th['queue'].qsize()

    if DEBUG:
        debug()
        raw_input('press any key to continue')

    print "[*]testing with " + str(th["THREADS_NUM"]) + " threads..."
    POC_T().run()


def debug():
    print "---conf---"
    print conf
    print "---paths---"
    print paths
    print "---th---"
    print th


if __name__ == "__main__":
    main()
