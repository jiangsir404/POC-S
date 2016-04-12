#!/usr/bin/env python
#
#  Parse command line arguments
#

import argparse
import sys
import os
import glob


def parse_args():
    parser = argparse.ArgumentParser(prog='POC-T',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='From i@cdxy.me http://www.cdxy.me',
                                     usage='POC-T.py [options]')

    parser.add_argument('-m', metavar='module_name', type=str, default='',
                        help='Select Module/POC name in ./module/')
    parser.add_argument('-f', metavar='filepath', type=str, default='',
                        help='Load targets from TargetFile')
    parser.add_argument('-i', metavar='int_string', type=str, default='',
                        help='-i [start_int]-[end_int]: test payloads from int(start) to int(end) with step 1.')
    parser.add_argument('-t', metavar='threads_num', type=int, default=10,
                        help='Num of scan threads for each scan process, 10 by default')
    parser.add_argument('-o', metavar='output', type=str, default='',
                        help='Output file path&name. default in ./output/')
    parser.add_argument('--show', default=False, action='store_true',
                        help='Show available module/POC names')
    parser.add_argument('--nF', default=True, action='store_false',
                        help='Disable file output.')
    parser.add_argument('--nS', default=True, action='store_false',
                        help='Disable screen output.')
    parser.add_argument('-v', action='version', version='%(prog)s 1.1    By cdxy (http://www.cdxy.me)')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()

    check_args(args)
    return args


def check_args(args):
    if args.show:
        module_name_list = glob.glob(r'./module/*.py')
        print '\nModule Num: ' + str(len(module_name_list) - 1)
        for each in module_name_list:
            _str = each.split('/')[-1].strip('.py')
            if _str not in ['__init__']:
                print _str
        sys.exit(0)

    if not args.m:
        msg = 'Use -m to select a module name.'
        raise Exception(msg)
    if args.m and not os.path.isfile("./module/" + args.m + ".py"):
        msg = 'module not exist.\nUse --show to view all available module names.'
        raise Exception(msg)

    if (not args.f and not args.i) or (args.f and args.i):
        msg = 'Use -f to set TargetFile or -i to set Payload.'
        raise Exception(msg)
    if args.f and not os.path.isfile(args.f):
        raise Exception('TargetFile not found: %s' % args.f)
    if args.i:
        help_str = "invalid input in [-i]\n Example: python POC-T -m test -i 1-100"
        try:
            _int = args.i.strip().split('-')
            if int(_int[0]) < int(_int[1]):
                pass
                # print "\n[*] Loading Payloads from " + _int[0] + " to " + _int[1] + " ..\n"
                # TODO
            else:
                print help_str
                sys.exit(0)
        except Exception, e:
            print e
            print help_str
            sys.exit(0)
