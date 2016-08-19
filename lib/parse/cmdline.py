#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import argparse
import sys
from lib.core.settings import VERSION


def cmdLineParser():
    parser = argparse.ArgumentParser(description='powered by cdxy <mail:i@cdxy.me> ',
                                     usage='\n  python POC-T.py [-T|-C] [-m NAME] [-s|-f|-i|-n|--api VALUE] [options]'
                                           '\n  python POC-T.py [-h|-v|--show|--update]'
                                           '\n\nexample:\n'
                                           '  python POC-T.py -T -m jboss-poc -s http://www.cdxy.me\n'
                                           '  python POC-T.py -T -m test -f ./dic/1-100.txt\n'
                                           '  python POC-T.py -C -m spider -i 1-100\n'
                                           '  python POC-T.py -C -m ./script/spider.py -n 10.0.0.0/24\n'
                                           '  python POC-T.py -T -m test --api --dork "port:21" --max-page 5\n'
                                           '  python POC-T.py -T -m test --api --query "solr country:cn" --limit 10 --offset 0',
                                     add_help=False)

    engine = parser.add_argument_group('engine')
    engine.add_argument('-T', default=False, action='store_true',
                        help='load Multi-Threaded engine')

    engine.add_argument('-C', default=False, action='store_true',
                        help='load Coroutine engine (single-threaded with asynchronous)')

    engine.add_argument('-t', metavar='NUM', type=int, default=10,
                        help='num of threads/concurrent, 10 by default')

    script = parser.add_argument_group('script')

    script.add_argument('-m', metavar='NAME', type=str, default='',
                        help='load script by name (-m jboss-rce) or path (-m ./script/jboss.py)')

    target = parser.add_argument_group('target mode')

    target.add_argument('-s', metavar='TARGET', type=str, default='',
                        help="scan a single target (e.g. www.wooyun.org)")
    target.add_argument('-f', metavar='FILE', type=str, default='',
                        help='load targets from targetFile (e.g. ./data/wooyun_domain)')
    target.add_argument('-i', metavar='START-END', type=str, default='',
                        help='generate targets from int(start) to int(end) (e.g. 1-100)')
    target.add_argument('-n', metavar='IP/MASK', type=str, default='',
                        help='load target IPs from IP/MASK. (e.g. 127.0.0.0/24)')
    target.add_argument('--api', default=False, action='store_true',
                        help='get targets with ZoomEye/Shodan/Censys API.')

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
                              help='show available script names in ./script/ and exit')
    optimization.add_argument('--browser', default=False, action='store_true',
                              help='Open notepad or web browser to view report after task finished.')
    optimization.add_argument('--debug', default=False, action='store_true',
                              help='show more details while running')
    optimization.add_argument('--update', default=False, action='store_true',
                              help='update POC-T from github')
    optimization.add_argument('-v', '--version', action='version', version=VERSION,
                              help="show program's version number and exit")
    optimization.add_argument('-h', '--help', action='help',
                              help='show this help message and exit')
    optimization.add_argument('-hc', '--helpCN', default=False, action='store_true',
                              help=u'打印中文帮助(show help message in Chinese)')

    ZoomeyeApi = parser.add_argument_group('ZoomEye API')
    ZoomeyeApi.add_argument("--dork", metavar='STRING', dest="dork", action="store", default=None,
                            help="ZoomEye dork used for search.")
    ZoomeyeApi.add_argument("--max-page", metavar='PAGE', dest="max_page", type=int, default=1,
                            help="(optional) Max page used in ZoomEye API (10 targets/Page, default:1).")
    ZoomeyeApi.add_argument("--search-type", metavar='TYPE', dest="search_type", action="store", default='host',
                            help="(optional) search type used in ZoomEye API, web or host (default:host)")

    ShodanAPI = parser.add_argument_group('Shodan API')
    ShodanAPI.add_argument("--query", metavar='STRING', dest="shodan_query", action="store", default=None,
                           help="Search query; identical syntax to the website")
    ShodanAPI.add_argument("--limit", metavar='LIMIT', dest="shodan_limit", type=int, default=100,
                           help="(optional) Number of results to return (default:100)")
    ShodanAPI.add_argument("--offset", metavar='OFFSET', dest="shodan_offset", type=int, default=0,
                           help="(optional) Search offset to begin getting results from (default:0)")

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args
