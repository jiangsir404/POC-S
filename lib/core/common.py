# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
import re
import sys
import time
from lib.core.data import *
from lib.core.log import CUSTOM_LOGGING, LOGGER_HANDLER
from lib.core.settings import BANNER, UNICODE_ENCODING, NULL, INVALID_UNICODE_CHAR_FORMAT
from lib.core.convert import stdoutencode
from thirdparty.termcolor.termcolor import colored
from thirdparty.odict.odict import OrderedDict


def setPaths():
    """
    Sets absolute paths for project directories and files
    """
    ROOT_PATH = paths['ROOT_PATH']
    paths['DATA_PATH'] = os.path.join(ROOT_PATH, "data")
    paths['MODULES_PATH'] = os.path.join(ROOT_PATH, "module")
    paths['OUTPUT_PATH'] = os.path.join(ROOT_PATH, "output")
    if not os.path.exists(paths['MODULES_PATH']):
        os.mkdir(paths['MODULES_PATH'])
    if not os.path.exists(paths['OUTPUT_PATH']):
        os.mkdir(paths['OUTPUT_PATH'])
    if not os.path.exists(paths['DATA_PATH']):
        os.mkdir(paths['DATA_PATH'])
    try:
        paths['WEAK_PASS'] = os.path.join(paths['DATA_PATH'], "pass100.txt")
        paths['LARGE_WEAK_PASS'] = os.path.join(paths['DATA_PATH'], "pass1000.txt")
        paths['UA_LIST_PATH'] = os.path.join(paths['DATA_PATH'], "user-agents.txt")
    except Exception, e:
        msg = 'Some files in ./data are missing, it may cause an issue\n'
        msg += 'Please use \'--update\' to get the complete program from github.com.'
        logger.log(CUSTOM_LOGGING.WARNING, msg)


def checkFile(filename):
    """
    @function Checks for file existence and readability
    """

    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except:
            valid = False

    if not valid:
        raise Exception("unable to read file '%s'" % filename)


def debugPause():
    if conf['DEBUG']:
        raw_input('[Debug] Press <Enter> to continue.')


def showDebugData():
    logger.log(CUSTOM_LOGGING.SYSINFO, '----conf---=\n%s' % conf)
    logger.log(CUSTOM_LOGGING.SYSINFO, '----paths---=\n%s' % paths)
    logger.log(CUSTOM_LOGGING.SYSINFO, '----th---=\n%s' % th)
    debugPause()


def banner():
    """
    Function prints banner with its version
    """
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    dataToStdout(_)


def dataToStdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """
    if conf['SCREEN_OUTPUT']:
        message = ""

        if isinstance(data, unicode):
            message = stdoutencode(data)
        else:
            message = data

        sys.stdout.write(setColor(message, bold))

        try:
            sys.stdout.flush()
        except IOError:
            pass
    return


def setColor(message, bold=False):
    retVal = message

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            retVal = colored(message, color=None, on_color=None, attrs=("bold",))

    return retVal


def pollProcess(process, suppress_errors=False):
    """
    Checks for process status (prints > if still running)
    """

    while True:
        message = '>'
        sys.stdout.write(message)
        try:
            sys.stdout.flush()
        except IOError:
            pass

        time.sleep(1)

        returncode = process.poll()

        if returncode is not None:
            if not suppress_errors:
                if returncode == 0:
                    # TODO　print导致线程资源不安全
                    print " done\n"
                elif returncode < 0:
                    print " process terminated by signal %d\n" % returncode
                elif returncode > 0:
                    print " quit unexpectedly with return code %d\n" % returncode
            break


def getSafeExString(ex, encoding=None):
    """
    Safe way how to get the proper exception represtation as a string
    (Note: errors to be avoided: 1) "%s" % Exception(u'\u0161') and 2) "%s" % str(Exception(u'\u0161'))
    """

    retVal = ex

    if getattr(ex, "message", None):
        retVal = ex.message
    elif getattr(ex, "msg", None):
        retVal = ex.msg

    return getUnicode(retVal, encoding=encoding)


def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return NULL

    if isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(
                        INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike(u'2')
    False
    """

    return isinstance(value, (list, tuple, set))


def sysquit(status=0):
    sys.stdout.write('\n')
    sys.stdout.flush()
    if status == 1:
        logger.error('User quit!')
    else:
        logger.info('System exit.')
    return


def getFileItems(filename, commentPrefix='#', unicode_=True, lowercase=False, unique=False):
    """
    @function returns newline delimited items contained inside file
    """

    retVal = list() if not unique else OrderedDict()

    checkFile(filename)

    try:
        with open(filename, 'r') as f:
            for line in (f.readlines() if unicode_ else f.xreadlines()):
                # xreadlines doesn't return unicode strings when codecs.open() is used
                if commentPrefix and line.find(commentPrefix) != -1:
                    line = line[:line.find(commentPrefix)]

                line = line.strip()

                if not unicode_:
                    try:
                        line = str.encode(line)
                    except UnicodeDecodeError:
                        continue

                if line:
                    if lowercase:
                        line = line.lower()

                    if unique and line in retVal:
                        continue

                    if unique:
                        retVal[line] = True

                    else:
                        retVal.append(line)

    except (IOError, OSError, MemoryError), ex:
        errMsg = "something went wrong while trying "
        errMsg += "to read the content of file '%s' ('%s')" % (filename, ex)
        raise Exception(errMsg)

    return retVal if not unique else retVal.keys()
