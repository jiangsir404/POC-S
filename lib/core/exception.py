# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'


class ToolkitBaseException(Exception):
    pass


class ToolkitDataException(ToolkitBaseException):
    pass


class ToolkitMissingPrivileges(ToolkitBaseException):
    pass


class ToolkitUserQuitException(ToolkitBaseException):
    pass


class ToolkitSystemException(ToolkitBaseException):
    pass


class ToolkitUnsupportedDBMSException(ToolkitBaseException):
    pass


class ToolkitUnsupportedFeatureException(ToolkitBaseException):
    pass


class ToolkitValueException(ToolkitBaseException):
    pass
