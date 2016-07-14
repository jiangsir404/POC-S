#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import random
import hashlib
from string import ascii_lowercase


def randomString(length=8):
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])


def randomMD5(hex=True):
    plain = randomString(3)
    m = hashlib.md5()
    m.update(plain)
    cipher = m.hexdigest() if hex else m.hexdigest()[8:-8]
    return [plain, cipher]
