#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

from setuptools import setup, find_packages
from lib.core.settings import VERSION, AUTHOR, MAIL, PROJECT, GIT_PAGE, LICENSE

setup(
    name=PROJECT,
    version=VERSION,
    keywords=('pentest', 'PoC', 'Exp', 'bruteforce', 'spider', 'POC-T'),
    description='POC-T: Pentest Over Concurrent Toolkit',
    license=LICENSE,
    install_requires=['gevent', 'requests', 'shodan'],
    url=GIT_PAGE,
    author=AUTHOR,
    author_email=MAIL,
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    platforms='any',
)
