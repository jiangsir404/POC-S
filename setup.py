#!/usr/bin/env python            
#coding:utf-8

from setuptools import setup, find_packages
import sys, os

version = '1.2'

setup(name='pocs',
      version=version,
      description="POC-T Stong Version POC-T加强版",
      long_description="""\
rivir""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='PoC,Exp,POC-T, POC-S, Pentest',
      author='rivir',
      author_email='rivirsir@163.com',
      url='https://github.com/jiangsir404/POC-S',
      license='',
      packages=find_packages(include=('*')),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'requests',
          'gevent',
          'shodan',
          'google-api-python-client'
      ],
      entry_points={
          "console_scripts": [
              "poc-s=pocs.pocs:main",
              "pocs=pocs.pocs:main"
          ]
      },
      )
