#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


DNSLOG_FIle = "../dnslog.json"
import json

def main():
    with open(DNSLOG_FIle) as f:
        dnslog_content = json.load(f)
    print(dnslog_content)

if __name__ == "__main__":
    main()
