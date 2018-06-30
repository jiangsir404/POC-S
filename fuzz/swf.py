#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests
import urlparse
import md5

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    arg = url

    FileList = []
    FileList.append(arg+'common/swfupload/swfupload.swf')
    FileList.append(arg+'adminsoft/js/swfupload.swf')
    FileList.append(arg+'statics/js/swfupload/swfupload.swf')
    FileList.append(arg+'images/swfupload/swfupload.swf')
    FileList.append(arg+'js/upload/swfupload/swfupload.swf')
    FileList.append(arg+'addons/theme/stv1/_static/js/swfupload/swfupload.swf')
    FileList.append(arg+'admin/kindeditor/plugins/multiimage/images/swfupload.swf')
    FileList.append(arg+'includes/js/upload.swf')
    FileList.append(arg+'js/swfupload/swfupload.swf')
    FileList.append(arg+'Plus/swfupload/swfupload/swfupload.swf')
    FileList.append(arg+'e/incs/fckeditor/editor/plugins/swfupload/js/swfupload.swf')
    FileList.append(arg+'include/lib/js/uploadify/uploadify.swf')
    FileList.append(arg+'lib/swf/swfupload.swf')

    md5_list = [
        '3a1c6cc728dddc258091a601f28a9c12',
        '53fef78841c3fae1ee992ae324a51620',
        '4c2fc69dc91c885837ce55d03493a5f5',        
    ]
    result = []
    for payload in FileList:
        try:
            header = dict()
            header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            r = requests.get(payload, headers=header, timeout=5)
            if r.status_code == 200:
                md5_value = md5.new(r.content).hexdigest()
                if md5_value in md5_list:
                    result.append(payload)
        except Exception:
            return False
    if result:
        return result