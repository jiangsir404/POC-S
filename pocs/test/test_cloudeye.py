#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Author: rivir
Date: 2020/2/22
"""
import sys
sys.path.append('../')
from plugin.cloudeye import CloudEye

c = CloudEye()
a = c.getRandomDomain('cdxy')
try:
    requests.get('http://' + a, timeout=1)
except Exception:
    pass
print c.verifyDNS(delay=0)
print c.verifyHTTP(delay=0)
print c.getDnsRecord(delay=0)
print c.getHttpRecord(delay=0)


if __name__ == "__main__":
    main()
