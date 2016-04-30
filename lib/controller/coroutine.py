# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import sys
from lib.core.data import th, conf, logger
try:
    from gevent import monkey

    monkey.patch_all()
    import gevent
# TODO gevent 针对https的请求会出现错误
except ImportError, e:
    sys.exit(logger.error(str(e) + '\nPlease run command: pip install -r requirements.txt\n'))
import time
import imp
from lib.utils.consle import getTerminalSize
from lib.core.enums import CUSTOM_LOGGING


class CoroutineEngine:
    def __init__(self):
        self.module_name = conf['MODULE_NAME']
        fp, pathname, description = imp.find_module(self.module_name, ["module"])
        self.module_obj = imp.load_module("_", fp, pathname, description)
        self.f_flag = conf['FILE_OUTPUT']
        self.s_flag = conf['SCREEN_OUTPUT']
        self.queue = th['queue']
        self.output = conf['OUTPUT_FILE_PATH']
        self.thread_count = self.threads_num = th['THREADS_NUM']
        self.single_mode = conf['SINGLE_MODE']
        self.scan_count = self.found_count = 0
        self.console_width = getTerminalSize()[0]
        self.console_width -=2
        self.is_continue = True
        self.found_single = False
    def _update_scan_count(self):
        self.scan_count += 1

    def _print_message(self, msg):
        sys.stdout.write('\r' + msg + ' ' * (self.console_width - len(msg)) + '\n\r')
        sys.stdout.flush()

    def _print_progress(self):
        msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
            self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
        sys.stdout.write('\r' + ' ' * (self.console_width - len(msg)) + msg)
        sys.stdout.flush()

    def _increase_scan_count(self):
        self.scan_count += 1

    def _increase_found_count(self):
        self.found_count += 1

    def _decrease_thread_count(self):
        self.thread_count -= 1

    def _output2file(self, msg):
        f = open(self.output, 'a')
        f.write(msg + '\n')
        f.close()

    def _single_mode(self, payload):
        self.is_continue = False
        self.found_single = True

    def _scan(self):
        while self.queue.qsize() > 0 and self.is_continue:
            payload = str(self.queue.get(timeout=1.0))
            poced = False

            try:
                poced = True if self.module_obj.poc(payload) else False
            except Exception, e:
                logger.log(CUSTOM_LOGGING.WARNING, e)
                self.is_continue = False

            if poced:
                self._increase_found_count()
                if self.s_flag:
                    self._print_message(payload)
                if self.f_flag:
                    self._output2file(payload)
                if self.single_mode:
                    self._single_mode(payload)
            self._update_scan_count()
            if self.s_flag:
                self._print_progress()

        if self.s_flag:
            self._print_progress()
        self._decrease_thread_count()

    def run(self):
        self.start_time = time.time()
        msg = 'Set the number of concurrent: %d' % self.threads_num
        logger.log(CUSTOM_LOGGING.SUCCESS, msg)
        while self.queue.qsize() > 0 and self.is_continue:
            gevent.joinall([gevent.spawn(self._scan) for i in xrange(0, self.threads_num) if
                            self.queue.qsize() > 0])
        if self.found_single:
            msg = "[single-mode] found!"
            sys.stdout.write('\n')
            sys.stdout.flush()
            logger.log(CUSTOM_LOGGING.SYSINFO, msg)

