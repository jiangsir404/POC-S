# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import censys.certificates

UID = "login for API key"
SECRET = "login for API secret"

certificates = censys.certificates.CensysCertificates(UID, SECRET)
fields = ["parsed.subject_dn", "parsed.fingerprint_sha256", "parsed.fingerprint_sha1"]

for c in certificates.search("current_valid_nss: true"):
    print c["parsed.subject_dn"]
