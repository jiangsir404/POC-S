# -*-coding:utf8-*-

import requests
import json
import MySQLdb


def info():
    pass


def exp():
    pass


def poc(str):
    url = 'http://space.bilibili.com/ajax/member/GetInfo?mid=' + str
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
    }

    jscontent = requests.get(url, headers=head, verify=False).content
    jsDict = json.loads(jscontent)
    if jsDict['status'] and jsDict['data']['sign']:
        jsData = jsDict['data']
        mid = jsData['mid']
        name = jsData['name']
        sign = jsData['sign']
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8')
            cur = conn.cursor()
            conn.select_db('bilibili')
            cur.execute(
                'INSERT INTO bilibili_user_info VALUES (%s,%s,%s,%s)', [mid, mid, name, sign])
            return True

        except MySQLdb.Error, e:
            pass
            # print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    else:
        # print "Pass: " + url
        pass
    return False
