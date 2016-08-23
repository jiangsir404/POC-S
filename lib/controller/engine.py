#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import sys
from lib.core.data import th, conf, logger

try:
    from gevent import monkey

    monkey.patch_all()
    import gevent
# TODO use monkey patch in script/*.py
except ImportError, e:
    logger.error(str(e) + '\nPlease run command: pip install -r requirements.txt\n')
    sys.exit(0)
import threading
import time
import traceback
from lib.core.common import dataToStdout
from lib.utils.consle import getTerminalSize
from lib.utils.versioncheck import PYVERSION
from lib.core.enums import CUSTOM_LOGGING, POC_RESULT_STATUS, ENGINE_MODE_STATUS


def initEngine():
    th.thread_mode = True if conf.ENGINE is ENGINE_MODE_STATUS.THREAD else False
    th.module_name = conf.MODULE_NAME
    th.f_flag = conf.FILE_OUTPUT
    th.s_flag = conf.SCREEN_OUTPUT
    th.output = conf.OUTPUT_FILE_PATH
    th.thread_count = th.threads_num = th.THREADS_NUM
    th.single_mode = conf.SINGLE_MODE
    th.scan_count = th.found_count = 0
    th.console_width = getTerminalSize()[0] - 2
    th.is_continue = True
    th.found_single = False
    th.start_time = time.time()
    setThreadLock()
    msg = 'Set the number of concurrent: %d' % th.threads_num
    logger.log(CUSTOM_LOGGING.SUCCESS, msg)


def singleMode():
    th.is_continue = False
    th.found_single = True


def scan():
    while 1:
        if th.thread_mode: th.load_lock.acquire()
        if th.queue.qsize() > 0 and th.is_continue:
            payload = str(th.queue.get(timeout=1.0))
            if th.thread_mode: th.load_lock.release()
        else:
            if th.thread_mode: th.load_lock.release()
            break
        try:
            # POC在执行时报错如果不被处理，线程框架会停止并退出
            status = th.module_obj.poc(payload)
            resultHandler(status, payload)
        except Exception:
            logger.log(CUSTOM_LOGGING.ERROR, 'Errors found in current script.')
            traceback.print_exc()
            th.is_continue = False
        changeScanCount(1)
        if th.s_flag:
            printProgress()
    if th.s_flag:
        printProgress()

    changeThreadCount(-1)


def run():
    initEngine()
    if conf.ENGINE is ENGINE_MODE_STATUS.THREAD:
        for i in range(th.threads_num):
            t = threading.Thread(target=scan, name=str(i))
            setThreadDaemon(t)
            t.start()
        # It can quit with Ctrl-C
        while 1:
            if th.thread_count > 0 and th.is_continue:
                time.sleep(0.01)
            else:
                break

    elif conf.ENGINE is ENGINE_MODE_STATUS.GEVENT:
        while th.queue.qsize() > 0 and th.is_continue:
            gevent.joinall([gevent.spawn(scan) for i in xrange(0, th.threads_num) if
                            th.queue.qsize() > 0])
    if th.found_single:
        msg = "[single-mode] found!"
        sys.stdout.write('\n')
        sys.stdout.flush()
        logger.log(CUSTOM_LOGGING.SYSINFO, msg)


def resultHandler(status, payload):
    if status is False or status is POC_RESULT_STATUS.FAIL:
        return
    elif status is POC_RESULT_STATUS.RETRAY:
        changeScanCount(-1)
        th.queue.put(payload)
        return
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        msg = payload
    else:
        # TODO handle this exception
        try:
            msg = str(status)
        except Exception, e:
            printMessage(e)
            return
    changeFoundCount(1)
    if th.s_flag:
        printMessage(msg)
    if th.f_flag:
        output2file(msg)
    if th.single_mode:
        singleMode()


def setThreadLock():
    if th.thread_mode:
        th.found_count_lock = threading.Lock()
        th.scan_count_lock = threading.Lock()
        th.thread_count_lock = threading.Lock()
        th.file_lock = threading.Lock()
        th.load_lock = threading.Lock()


def setThreadDaemon(thread):
    # Reference: http://stackoverflow.com/questions/190010/daemon-threads-explanation
    if PYVERSION >= "2.6":
        thread.daemon = True
    else:
        thread.setDaemon(True)


def changeFoundCount(num):
    if th.thread_mode: th.found_count_lock.acquire()
    th.found_count += num
    if th.thread_mode: th.found_count_lock.release()


def changeScanCount(num):
    if th.thread_mode: th.scan_count_lock.acquire()
    th.scan_count += num
    if th.thread_mode: th.scan_count_lock.release()


def changeThreadCount(num):
    if th.thread_mode: th.thread_count_lock.acquire()
    th.thread_count += num
    if th.thread_mode: th.thread_count_lock.release()


def printMessage(msg):
    dataToStdout('\r' + msg + ' ' * (th.console_width - len(msg)) + '\n\r')


def printProgress():
    msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
        th.found_count, th.queue.qsize(), th.scan_count, time.time() - th.start_time)
    out = '\r' + ' ' * (th.console_width - len(msg)) + msg
    dataToStdout(out)


def output2file(msg):
    if th.thread_mode: th.file_lock.acquire()
    f = open(th.output, 'a')
    f.write(msg + '\n')
    f.close()
    if th.thread_mode: th.file_lock.release()
