#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

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


class ToolkitValueException(ToolkitBaseException):
    pass


class ToolkitPluginException(ToolkitBaseException):
    pass


class RegisterException(Exception):
    pass


class RegisterValueException(RegisterException):
    pass


class RegisterDataException(RegisterException):
    pass


class RegisterMutexException(RegisterException):
    pass
