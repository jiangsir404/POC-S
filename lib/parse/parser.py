# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import argparse
import sys

from lib.parse.handler import checkArgs, setArgs
from lib.core.settings import VERSION

def parseArgs():
    parser = argparse.ArgumentParser(prog='POC-T',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='powered by cdxy <mail:i@cdxy.me> ',
                                     usage='\n  python POC-T.py [-T|-C] [-m NAME] [-f|-i|-n VALUE] [options]'
                                           '\n  python POC-T.py [-h|-v|--show|--update]'
                                           '\n\nexample:\n'
                                           '  python POC-T.py -T -m test -f ./dic/1-100.txt\n'
                                           '  python POC-T.py -C -m test -i 1-100\n'
                                           '  python POC-T.py -C -m spider -n 10.0.0.0/24',
                                     add_help=False)

    engine = parser.add_argument_group('engine')
    engine.add_argument('-T', default=False, action='store_true',
                        help='load Multi-Threaded engine')

    engine.add_argument('-C', default=False, action='store_true',
                        help='load Coroutine engine (single-threaded with asynchronous)')

    engine.add_argument('-t', metavar='NUM', type=int, default=10,
                        help='num of threads/concurrent, 10 by default')

    module = parser.add_argument_group('module')

    module.add_argument('-m', metavar='NAME', type=str, default='',
                        help='select Module/POC name in ./module/ (without ".py")')

    target = parser.add_argument_group('target mode')
    target.add_argument('-f', metavar='FILE', type=str, default='',
                        help='load targets from TargetFile (e.g. ./data/wooyun_domain)')
    target.add_argument('-i', metavar='START-END', type=str, default='',
                        help='generate payloads from int(start) to int(end) (e.g. 1-100)')
    target.add_argument('-n', metavar='IP/MASK', type=str, default='',
                        help='load target IPs from IP/MASK. (e.g. 127.0.0.0/24)')
    optimization = parser.add_argument_group('optimization')

    optimization.add_argument('-o', metavar='FILE', type=str, default='',
                              help='output file path&name. default in ./output/')
    optimization.add_argument('--single', default=False, action='store_true',
                              help='exit after finding the first victim/password.')
    optimization.add_argument('--nF', default=True, action='store_false',
                              help='disable file output')
    optimization.add_argument('--nS', default=True, action='store_false',
                              help='disable screen output')
    optimization.add_argument('--show', default=False, action='store_true',
                              help='show available module/POC names and exit')
    optimization.add_argument('--browser', default=False, action='store_true',
                              help='Open notepad or web browser to view report after task was finished.')
    optimization.add_argument('--debug', default=False, action='store_true',
                              help='show more details while running')
    optimization.add_argument('--update', default=False, action='store_true',
                              help='update POC-T from github')
    optimization.add_argument('-h', '--help', action='help',
                              help='show this help message and exit')
    optimization.add_argument('-v', '--version', action='version', version=VERSION,
                              help="show program's version number and exit")

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    checkArgs(args)
    setArgs(args)
