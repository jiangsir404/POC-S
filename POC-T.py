# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# From i@cdxy.me http://www.cdxy.me

import Queue
import sys
import threading
import time
import optparse
import glob
import imp
from lib.consle_width import getTerminalSize
from lib.cmdline import parse_args


class POC_T:
    def __init__(self, threads_num, module_name, filepath, output, f_flag, s_flag):

        # 动态加载外部模块
        fp, pathname, description = imp.find_module(module_name, ["module"])
        self.module_obj = imp.load_module("_", fp, pathname, description)
        self.filepath = filepath
        self.cancel_output = False
        self.cancel_print = False
        self.f_flag = f_flag
        self.s_flag = s_flag
        self.output = output if output else \
            './output/' \
            + time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time())) \
            + module_name \
            + '.txt'

        self.thread_count = self.threads_num = threads_num
        self.scan_count = self.found_count = 0
        self.lock = threading.Lock()
        self.console_width = getTerminalSize()[0]
        self.console_width -= 2  # Cal width when starts up
        self._load_pass()
        self.headers = {  # TODO
                          "Content-Type": "application/x-www-form-urlencoded"
                          }

    # 读入队列
    def _load_pass(self):
        self.queue = Queue.Queue()
        with open(self.filepath) as f:
            for line in f:
                sub = line.strip()
                if sub:
                    self.queue.put(sub)

    def _update_scan_count(self):
        self.lock.acquire()
        self.scan_count += 1
        self.lock.release()

    def _print_progress(self):
        self.lock.acquire()
        msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
            self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
        sys.stdout.write('\r' + ' ' * (self.console_width - len(msg)) + msg)
        sys.stdout.flush()
        self.lock.release()

    def _scan(self):
        while self.queue.qsize() > 0:
            payload = self.queue.get(timeout=1.0)
            poced = False

            try:
                if self.module_obj.poc(payload):
                    poced = True
                else:
                    pass
            except:
                pass

            if poced:  # 不能把open语句放在try块里，因为当打开文件出现异常时，文件对象file_object无法执行close()方法
                self.lock.acquire()
                self.found_count += 1
                if self.f_flag:
                    f = open(self.output, 'a')
                    f.write(payload + '\n')
                    f.close()
                self.lock.release()
            self._update_scan_count()

            if self.s_flag:
                self._print_progress()

        if self.s_flag:
            self._print_progress()
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def run(self):
        self.start_time = time.time()
        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            t.setDaemon(True)
            t.start()
        while self.thread_count > 0:
            time.sleep(0.01)


if __name__ == '__main__':
    args = parse_args()
    d = POC_T(threads_num=args.t,
              module_name=args.m,
              filepath=args.f,
              output=args.o,
              f_flag=args.nF,
              s_flag=args.nS
              )
    d.run()
