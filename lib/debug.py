#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
POC-T functional testing script
"""

valid = """
-h
--help
-hc
-v
--version
--show
-eC -s test -iA 1-10
-eT -s test -n 127.0.0.0/28 --browser --nS
-eT -s test -f ./data/wooyun_domain --single -o test_ans.txt
-eC -s bingc -t 9 -n 139.129.132.0/28 --nF --debug
-eT -s solr-unauth -aZ "solr country:cn" --max-page 2 --search-type host
-eT -s bingc.py -aS "solr country:cn" --offset 10 --limit 5

"""

invalid = """
-m test
-eT --nF
-eT -s --api
-eT -s -f -n
-eT -s -f -n -iA --api
-eT -eC -s test -iA 1-10
-eT -t -1 -s test -iA 1-10
-eC -s test -iA -1-10
-eC -s test -iA a-100
-eC -s test -iA 5-1
-eT -s test213zdf -iA 1-10
-eT -s test -iA 1-10 --nF -o aaa.txt
-eT -s test -iA 1-10 --nF --browser
-eT -s test -aZ "test" --query "test"
-eT -s test -iA 1-10 -n 127.0.0.0/30
-eT -s test -iAS 111 -f test.txt
-eT -s test -iA 1-10 -aZ "country:cn" --max-page 0
-eT -s test -iA 1-10 -aZ "country:cn" --max-page defs
-eT -s test -iA 1-10 -aZ "country:cn" --max-page 1 --search-type aaa
-eT -s test -iA 1-10 -aS "country:cn" --offset -1
-eT -s test -iA 1-10 -aS "country:cn" --offset asdsafse
-eT -s test -iA 1-10 -aS "country:cn" --limit 0
-eT -s test -iA 1-10 -aS "country:cn" --limit -1
-eT -s test -iA 1-10 -aS "country:cn" --limit afefea
-eT -s ./test
-eT -s /
"""

scripts_with_plugin = """
bingc 139.129.132.156
confluence-file-read www.cdxy.me
jboss-rce www.cdxy.me
solr-unauth http://36.110.167.60:8080
"""

header = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T
"""

import os


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
                a = ''.join(open(child).readlines()[:4]).replace('\n', '')
                if a != header.replace('\n', ''):
                    raise Exception('unformed header in: ' + child)


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    headerCheck(root_dir)

    os.chdir(root_dir)
    base = 'python POC-T.py '

    print '\n\n==== Testing features ====\n\n'
    os.system('python3 POC-T.py')
    os.system('python POC-T.py')
    for each in valid.splitlines():
        if len(each) > 1:
            print '[*] ' + base + each.strip()
            try:
                os.system(base + each.strip())
            except Exception, e:
                print e

    print '\n\n==== Testing invalid args ====\n\n'
    for each in invalid.splitlines():
        if len(each) > 1:
            print '[*] ' + base + each.strip()
            try:
                os.system(base + each.strip())
            except Exception, e:
                print(e)

    print '\n\n==== Testing Scripts & Plugins ====\n\n'
    for each in scripts_with_plugin.splitlines():
        if len(each) > 1:
            _l = each.strip().split(' ')
            command = 'python POC-T.py -T -t 1 -s %s -s %s --nF' % (str(_l[0]), str(_l[1]))
            print '[*] ' + command
            os.system(command)

    if os.path.isfile('test_ans.txt'):
        os.remove('test_ans.txt')
