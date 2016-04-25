# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import argparse
import sys

from lib.parse.handler import check_args, set_args


def parse_args():
    parser = argparse.ArgumentParser(prog='POC-T',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='From i@cdxy.me http://www.cdxy.me',
                                     usage='POC-T.py [-T|-C] [-m] [-f|-i|-n] [options]\n'
                                           '\nExample:\n'
                                           'python POC-T.py -T -m test -f ./dic/1-100.txt\n'
                                           'python POC-T.py -C -m test -i 1-100\n'
                                           'python POC-T.py -C -m spider -n 10.0.0.0/24')

    engine = parser.add_argument_group('engine')
    engine.add_argument('-T', default=False, action='store_true',
                        help='load Multi-Threaded engine')

    engine.add_argument('-C', default=False, action='store_true',
                        help='load Coroutine engine (single-threaded with asynchronous)')

    engine.add_argument('-t', metavar='[num]', type=int, default=10,
                        help='num of threads/concurrent, 10 by default')

    module = parser.add_argument_group('module')

    module.add_argument('-m', metavar='[module]', type=str, default='',
                        help='select Module/POC name in ./module/')

    target = parser.add_argument_group('target mode')
    target.add_argument('-f', metavar='[target]', type=str, default='',
                        help='load targets from TargetFile')
    target.add_argument('-i', metavar='[start]-[end]', type=str, default='',
                        help='generate payloads from int(start) to int(end)')
    target.add_argument('-n', metavar='[network]', type=str, default='',
                        help='load target IPs from IP/MASK. eg. 127.0.0.0/30')
    optimization = parser.add_argument_group('optimization')

    optimization.add_argument('-o', metavar='[output]', type=str, default='',
                              help='output file path&name. default in ./output/')
    optimization.add_argument('--single', default=False, action='store_true',
                              help='exit after finding the first victim/password.')
    optimization.add_argument('--nF', default=True, action='store_false',
                              help='disable file output')
    optimization.add_argument('--nS', default=True, action='store_false',
                              help='disable screen output')
    optimization.add_argument('--show', default=False, action='store_true',
                        help='show available module/POC names and exit')
    optimization.add_argument('--debug', default=False, action='store_true',
                        help='show more details while running')
    optimization.add_argument('--update', default=False, action='store_true',
                        help='update POC-T from github')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    check_args(args)
    set_args(args)
