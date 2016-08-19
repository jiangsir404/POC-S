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
--helpCn
-v
--version
--show
-C -m test -i 1-10
-T -m test -n 127.0.0.0/28 --browser --nS
-T -m test -f ./data/wooyun_domain --single -o test_ans.txt
-C -m bingc -t 9 -n 139.129.132.0/28 --nF --debug
-T -m solr-unauth --api --dork "solr country:cn" --max-page 2 --search-type host
-T -m bingc.py --api --query "solr country:cn" --offset 10 --limit 5

"""

invalid = """
-m test
-T --nF
-T -s --api
-T -s -f -n
-T -s -f -n -i --api
-T -C -m test -i 1-10
-T -t -1 -m test -i 1-10
-C -m test -i -1-10
-C -m test -i a-100
-C -m test -i 5-1
-T -m test213zdf -i 1-10
-T -m test -i 1-10 --nF -o aaa.txt
-T -m test -i 1-10 --nF --browser
-T -m test --api --dork "test" --query "test"
-T -m test -i 1-10 -n 127.0.0.0/30
-T -m test -s 111 -f test.txt
-T -m test -i 1-10 --api --dork "country:cn" --max-page 0
-T -m test -i 1-10 --api --dork "country:cn" --max-page defs
-T -m test -i 1-10 --api --dork "country:cn" --max-page 1 --search-type aaa
-T -m test -i 1-10 --api --query "country:cn" --offset -1
-T -m test -i 1-10 --api --query "country:cn" --offset asdsafse
-T -m test -i 1-10 --api --query "country:cn" --limit 0
-T -m test -i 1-10 --api --query "country:cn" --limit -1
-T -m test -i 1-10 --api --query "country:cn" --limit afefea
-T -m ./test
-T -m /
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
            command = 'python POC-T.py -T -t 1 -m %s -s %s --nF' % (str(_l[0]), str(_l[1]))
            print '[*] ' + command
            os.system(command)

    if os.path.isfile('test_ans.txt'):
        os.remove('test_ans.txt')
