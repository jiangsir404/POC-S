#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urlparse

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    
def audit(arg):
    parse = urlparse.urlparse(arg)
    url = "%s://%s/"%(parse.scheme,parse.netloc)
    arg = parse.netloc
    dirs = '''wwwroot.rar
wwwroot.zip
wwwroot.tar
wwwroot.tar.gz
web.rar
web.zip
web.tar
web.tar
ftp.rar
ftp.zip
ftp.tar
ftp.tar.gz
data.rar
data.zip
data.tar
data.tar.gz
admin.rar
admin.zip
admin.tar
admin.tar.gz
www.rar
www.zip
www.tar
www.tar.gz
flashfxp.rar
flashfxp.zip
flashfxp.tar
flashfxp.tar.gz
'''
    host_keys = arg.split(".")
    listFile = []
    for i in dirs.strip().splitlines():
        listFile.append(i)
    for key in host_keys:
        if key is '':
            host_keys.remove(key)
            continue
        if '.' in key:
            new = key.replace('.',"_")
            host_keys.append(new)
    host_keys.append(arg)
    for i in host_keys:
        new = "%s.rar"%(i)
        listFile.append(new)
        new = "%s.zip" % (i)
        listFile.append(new)
        new = "%s.tar.gz" % (i)
        listFile.append(new)
        new = "%s.tar" % (i)
        listFile.append(new)

    warning_list = []
    for payload in listFile:
        loads = url + payload
        try:
            header = dict()
            header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            r = requests.get(loads, headers=header, timeout=5)

            if r.status_code == 200 and "Content-Type" in r.headers and "application" in r.headers["Content-Type"] :
                warning_list.append("[BAKFILE] " + loads)
        except Exception:
            pass
        
    # In order to  solve the misreport
    if len(warning_list) > 6:
        return False
    else:
        return warning_list