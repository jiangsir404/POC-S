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
                                     usage='POC-T.py [-m] [-f or -i] [options]\n'
                                           '\nExample:\n'
                                           'python POC-T.py -m test -f ./dic/1-100.txt\n'
                                           'python POC-T.py -m test -i 1-100')

    parser.add_argument('-m', metavar='[module]', type=str, default='',
                        help='select Module/POC name in ./module/')
    parser.add_argument('-f', metavar='[target]', type=str, default='',
                        help='load targets from TargetFile')
    parser.add_argument('-i', metavar='[start]-[end]', type=str, default='',
                        help='generate payloads from int(start) to int(end)')
    parser.add_argument('-t', metavar='[threads]', type=int, default=10,
                        help='num of scan threads, 10 by default')
    parser.add_argument('-o', metavar='[output]', type=str, default='',
                        help='output file path&name. default in ./output/')

    parser.add_argument('--nF', default=True, action='store_false',
                        help='disable file output')
    parser.add_argument('--nS', default=True, action='store_false',
                        help='disable screen output')
    parser.add_argument('--show', default=False, action='store_true',
                        help='show available module/POC names and exit')
    parser.add_argument('--info', default=False, action='store_true',
                        help='show module/POC info and exit')
    parser.add_argument('-v', action='version', version='%(prog)s 1.1    By cdxy (http://www.cdxy.me)')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()

    check_args(args)
    return args


def check_args(args):
    module = args.m
    f = args.f
    i = args.i
    show = args.show

    if show:
        module_name_list = glob.glob(r'./module/*.py')
        print '\nNum: ' + str(len(module_name_list) - 1)
        print 'Module Name:'
        for each in module_name_list:
            # match both on Win & Linux
            _str = each.split('/')[-1].split('\\')[-1].strip('.py')
            if _str not in ['__init__']:
                print '  '+_str
        print '\nSystem exit!'
        sys.exit(0)

    if not module:
        msg = 'Use -m to select a module name.'
        print msg+'\nSystem exit!'
        sys.exit(0)

    if module and not os.path.isfile("./module/" + module + ".py"):
        msg = 'module not exist.\nUse --show to view all available module names.'
        print msg+'\nSystem exit!'
        sys.exit(0)

    if (not f and not i) or (f and i):
        msg = 'Use -f to set TargetFile or -i to set Payload.'
        print msg+'\nSystem exit!'
        sys.exit(0)

    if f and not os.path.isfile(f):
        msg = 'TargetFile not found: %s' % f
        print msg+'\nSystem exit!'
        sys.exit(0)

    if i:
        help_str = "invalid input in [-i]\n Example: python POC-T -m test -i 1-100"
        try:
            _int = i.strip().split('-')
            if int(_int[0]) < int(_int[1]):
                if int(_int[1])-int(_int[0]) >1000000:
                    print 'Loading %d Payloads...' % (int(_int[1])-int(_int[0]))
                    a = raw_input('Maybe its too much, continue? [Y/n]')
                    if a in ('','Y','y','yes'):
                        pass
                    else:
                        print 'User quit!'
                        sys.exit(0)
            else:
                print help_str+'\nSystem exit!'
                sys.exit(0)
        except Exception, e:
            print e
            print help_str+'\nSystem exit!'
            sys.exit(0)
