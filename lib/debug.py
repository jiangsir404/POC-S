#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
POC-T functional testing script
"""

auto = """

# help
-h;powered by cdxy <mail:i@cdxy.me>
--help;powered by cdxy <mail:i@cdxy.me>

# version
-v;2.
--version;2.

# show
--show;Script Name

# --browser --single -iA -iN -iS -iF
-s test;[-] Please load targets
-s test -iA 1-10 --single;[*] [single-mode] found!
-s test -iN 10.10.0/30 --browser -oF;[-] [--browser] is based on file output
-s test -iS "http://test.com" --browser;[*] System exit.
-s test -iF data/pass100.txt -t 50 -oF;concurrent: 50;[*] System exit.

# -s
-iA 1-10;Use -s to load script
-s 1234567890 -iS aaa;Script [1234567890.py] not exist
-s test -iS aaa;[*] System exit.
-s test.py -iS aaa;[*] System exit.
-s script/test.py -iS aaa;[*] System exit.
-s ./ -iS aaa;[-] [./] not a file.

# -eT -eC -t
-eT -s test -iA 1-10 -t 5 -oF;concurrent: 5;[*] System exit.
-eT -s test -iF data/pass100.txt -t 50 -oF;concurrent: 50;[*] System exit.
-eT -s test -iA 1-10 -t 500 -oF;range: 1 to 100
-eG -s test -iS http://sss.com -oF;[*] System exit

# -oS
-s test -iS aaa;by cdxy mail:i@cdxy.me };[*] System exit.
-s test -iS aaa -oS;[*] System exit.$mail:i@cdxy.me }

# --limit -aS -aZ -aG
-s test -aS 1 --limit=0;[-] Invalid value in [--limit]
-s test -aS 1 --limit=2;[+] Total: 2;[*] System exit.
-s test -aZ 1 --limit=2;[+] Total: 10;[*] System exit.
-s test -aZ 1 --limit=10;[+] Total: 10;[*] System exit.
-s test -aZ 1 --limit=11;[+] Total: 20;[*] System exit.
-s test -aG 1 --limit=2;[+] Total: 10;[*] System exit.
-s test -aG 1 --limit=10;[+] Total: 10;[*] System exit.
-s test -aG 1 --limit=11;[+] Total: 20;[*] System exit.
-s test -aG faefafw32qtfafw3;[+] Total: 0;[*] System exit.

# --offset
-s test -aS 1 --offset=0;[*] System exit.
-s test -aS 1 --offset=10;[*] System exit.

# --search-type
-s test -aZ 1 --search-type "hello";[-] Invalid value in [--search-type]
-s test -aZ 1 --search-type 111;[-] Invalid value in [--search-type]
-s test -aZ 1 --search-type web;[*] System exit.
-s test -aZ 1 --search-type host;[*] System exit.
-s test -aZ 1 --search-type web,host;[-] Invalid value in [--search-type]

# --gproxy
-s test -aG 1 --gproxy="http 127.0.0.1 1111";[-] Unable to connect Google
-s test -aG 1 --gproxy="http 127.0.0.1";[-] SyntaxError in GoogleProxy string
-s test -aG 1 --gproxy="1 127.0.0.1 1";[-] Invalid proxy-type
-s test -aG 1 --gproxy="http 127.0.0.1 fa";[-] Invalid port in GoogleProxy string
-s test -aG 1 --gproxy="http 127.0.0.1 1894";[*] System exit.
-s test -aG 1 --gproxy="sock5 127.0.0.1 7070";[*] System exit.
-s test -aG 1 --gproxy "http 127.0.0.1 23124";[-] Unable to connect Google

# output
-s test -iA 1-10 -o _checko.txt;[*] System exit.
-s test -iA 1-10 -o _checko1.txt -oF;[-] Cannot use [-oF] and [-o] together
-s test -iA 1-10 -o _checko2.txt -oS;[*] System exit.


# scripts

"""

header = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author"""

import os
import subprocess


def headerCheck(path):
    parents = os.listdir(path)
    for parent in parents:
        if parent == 'thirdparty':
            continue
        child = os.path.join(path, parent)
        if os.path.isdir(child):
            headerCheck(child)
        elif os.path.isfile(child):
            if child.endswith('.py'):
                if open(child).read().startswith(header):
                    pass
                else:
                    print 'Invalid header in %s' % child


def autoCheckResult(output, error, expect, unexpect):
    for each in expect:
        if each in output or each in error:
            pass
        else:
            return False
    for each in unexpect:
        if each in output or each in error:
            return False
        else:
            pass
    return True


def autoCheck():
    base = 'python POC-T.py '
    for each in auto.split('\n'):
        if not each or each.startswith('#'):
            continue
        u = each.split('$')[1:]
        each = each.split('$')[0]
        c = each.split(';')[0]
        r = each.split(';')[1:]

        command = base + c
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        o = process.stdout.read()
        e = process.stderr.read()
        if autoCheckResult(o, e, r, u):
            pass
        else:
            print command


def checkInvalidVersion():
    command = 'python3 POC-T.py -h'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    o = process.stdout.read()
    e = process.stderr.read()
    if autoCheckResult(o, e, ['[CRITICAL] incompatible Python version'], []):
        pass
    else:
        print command


def checkOutput(base_path):
    target1 = os.path.join(base_path, '_checko.txt')
    target2 = os.path.join(base_path, '_checko1.txt')
    target3 = os.path.join(base_path, '_checko2.txt')
    try:
        if len(open(target1).read()) and not os.path.isfile(target2) and len(open(target3).read()):
            os.remove(target1)
            os.remove(target3)
        else:
            print '!!!failed!!!'
    except IOError:
        print '!!!failed!!!'


def debugMain():
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(root_dir)
        print '>>> base-dir [%s]' % root_dir

        print '>>> start header check'
        headerCheck(root_dir)

        print '>>> start invalid-version check'
        checkInvalidVersion()

        print '>>> start command check'
        autoCheck()

        print '>>> start output check'
        checkOutput(root_dir)

    except KeyboardInterrupt:
        exit('User quit!')
    return


if __name__ == '__main__':
    debugMain()
