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


class POC_T:
    def __init__(self, threads_num, module_name, filepath, output):

        # 动态加载外部模块
        fp, pathname, description = imp.find_module(module_name, ["module"])
        self.module_obj = imp.load_module("_", fp, pathname, description)

        self.filepath = filepath

        self.cancel_output = False
        self.output = output if output else \
            './output/' \
            + time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time())) \
            + module_name \
            + '.txt'
        if self.output in ['N', 'n']:
            self.cancel_output = True

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
                if not self.cancel_output:
                    f = open(self.output, 'a')
                    f.write(payload + '\n')
                    f.close()
                self.lock.release()
            self._update_scan_count()
            self._print_progress()
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

    print "\n[------POC-T  version 1.0------]  \n From i@cdxy.me http://www.cdxy.me\n"
    parser = optparse.OptionParser('Usage: %prog [options] -m [module] -f [filepath]\n'
                                   'Example: python POC-T.py -t 20 -m ssh-brute -f ./iplist.txt')

    parser.add_option('-m', dest='module_name', default=None,
                      type='string', help='select module/POC name in ./module/')
    parser.add_option('-f', dest='filepath', default=None,
                      type='string', help='Input file path&name.')
    parser.add_option('-t', dest='threads_num',
                      default=10, type='int',
                      help='Number of threads. default = 10')
    parser.add_option('-o', dest='output',
                      type='string', help='Output file path&name. default in ./output/')
    parser.add_option('--show', dest='show_module_name', default=False,
                      action='store_true', help='Show available module/POC names')

    (options, args) = parser.parse_args()
    if not options.module_name or not options.filepath:
        parser.print_help()
        sys.exit(0)

    if options.show_module_name:
        module_name_list = glob.glob(r'./module/*.py')
        print 'Num: ' + str(len(module_name_list))
        for each in module_name_list:
            print each.split('/')[-1].strip('.py')
        parser.print_help()
        sys.exit(0)

    d = POC_T(threads_num=options.threads_num,
              module_name=options.module_name,
              filepath=options.filepath,
              output=options.output)
    d.run()
