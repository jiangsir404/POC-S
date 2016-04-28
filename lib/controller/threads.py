# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import threading
import time
import imp
import sys
from lib.core.data import th, conf, logger
from lib.utils.consle import getTerminalSize
from lib.utils.versioncheck import PYVERSION
from lib.core.enums import CUSTOM_LOGGING


class ThreadsEngine:
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
        self.num_lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.single_lock = threading.Lock()
        self.load_lock = threading.Lock()
        self.print_lock = threading.Lock()
        self.console_width = getTerminalSize()[0]
        self.console_width -= 2
        self.is_continue = True
        self.found_single = False

    def _update_scan_count(self):
        self.num_lock.acquire()
        self.scan_count += 1
        self.num_lock.release()

    def _print_message(self, msg):
        self.print_lock.acquire()
        sys.stdout.write('\r' + msg + ' ' * (self.console_width - len(msg)) + '\n\r')
        sys.stdout.flush()
        self.print_lock.release()

    def _print_progress(self):
        self.print_lock.acquire()
        msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
            self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
        sys.stdout.write('\r' + ' ' * (self.console_width - len(msg)) + msg)
        sys.stdout.flush()
        self.print_lock.release()

    def _increase_scan_count(self):
        self.num_lock.acquire()
        self.scan_count += 1
        self.num_lock.release()

    def _increase_found_count(self):
        self.num_lock.acquire()
        self.found_count += 1
        self.num_lock.release()

    def _decrease_thread_count(self):
        self.num_lock.acquire()
        self.thread_count -= 1
        self.num_lock.release()

    def _output2file(self, msg):
        self.file_lock.acquire()
        f = open(self.output, 'a')
        f.write(msg + '\n')
        f.close()
        self.file_lock.release()

    def _set_daemon(self, thread):
        # Reference: http://stackoverflow.com/questions/190010/daemon-threads-explanation
        if PYVERSION >= "2.6":
            thread.daemon = True
        else:
            thread.setDaemon(True)

    def _single_mode(self, payload):
        self.single_lock.acquire()
        self.is_continue = False
        self.found_single = True
        self.single_lock.release()

    def _scan(self):
        while 1:
            self.load_lock.acquire()
            if self.queue.qsize() > 0 and self.is_continue:
                payload = str(self.queue.get(timeout=1.0))
                self.load_lock.release()
            else:
                self.load_lock.release()
                break

            poced = False
            try:
                poced = True if self.module_obj.poc(payload) else False
            except Exception, e:
                print e
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
        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            self._set_daemon(t)
            t.start()
        # It can quit with Ctrl-C
        try:
            while self.thread_count > 0:
                time.sleep(0.01)
            if self.found_single:
                msg = "[single-mode] found!"
                sys.stdout.write('\n')
                sys.stdout.flush()
                logger.log(CUSTOM_LOGGING.SYSINFO, msg)
        except KeyboardInterrupt, e:
            logger.log(CUSTOM_LOGGING.ERROR, 'User quit!')
