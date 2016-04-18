# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

from lib.parse.parser import parse_args
from lib.controller.loader import load_payloads
from lib.controller.threads import POC_T
from lib.core.common import setPath
from lib.core.data import paths, th, conf
from lib.core.settings import DEBUG


def main():
    setPath()
    parse_args()
    load_payloads()

    if DEBUG:
        debug()

    POC_T().run()


def debug():
    print "---conf---"
    print conf
    print "---paths---"
    print paths
    print "---th---"
    print th
    print "---Queue_size---"
    print th['queue'].qsize()


if __name__ == "__main__":
    main()
