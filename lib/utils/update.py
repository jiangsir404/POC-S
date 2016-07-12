#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import locale
import os
import re
import sys
from subprocess import PIPE
from subprocess import Popen as execute
from lib.core.common import getSafeExString
from lib.core.common import pollProcess
from lib.core.data import conf
from lib.core.data import logger
from lib.core.data import paths
from lib.core.settings import GIT_REPOSITORY
from lib.core.settings import IS_WIN
from lib.core.revision import getRevisionNumber


def update():
    if not conf.UPDATE:
        return

    success = False

    if not os.path.exists(os.path.join(paths.ROOT_PATH, ".git")):
        errMsg = "not a git repository. Please checkout the 'Xyntax/POC-T' repository "
        errMsg += "from GitHub (e.g. 'git clone https://github.com/Xyntax/POC-T.git POC-T')"
        logger.error(errMsg)
    else:
        infoMsg = "updating POC-T to the latest development version from the "
        infoMsg += "GitHub repository"
        logger.info(infoMsg)

        debugMsg = "POC-T will try to update itself using 'git' command"
        logger.debug(debugMsg)

        logger.info("update in progress ")

        try:
            process = execute("git checkout . && git pull %s HEAD" % GIT_REPOSITORY, shell=True, stdout=PIPE,
                              stderr=PIPE, cwd=paths.ROOT_PATH.encode(
                    locale.getpreferredencoding()))  # Reference: http://blog.stastnarodina.com/honza-en/spot/python-unicodeencodeerror/
            pollProcess(process, True)
            stdout, stderr = process.communicate()
            success = not process.returncode
        except (IOError, OSError), ex:
            success = False
            stderr = getSafeExString(ex)

        if success:
            _ = getRevisionNumber()
            logger.info("%s the latest revision '%s'" % ("already at" if "Already" in stdout else "updated to", _))
        else:
            if "Not a git repository" in stderr:
                errMsg = "not a valid git repository. Please checkout the 'Xyntax/POC-T' repository "
                errMsg += "from GitHub (e.g. 'git clone https://github.com/Xyntax/POC-T.git POC-T')"
                logger.error(errMsg)
            else:
                logger.error("update could not be completed ('%s')" % re.sub(r"\W+", " ", stderr).strip())

    if not success:
        if IS_WIN:
            infoMsg = "for Windows platform it's recommended "
            infoMsg += "to use a GitHub for Windows client for updating "
            infoMsg += "purposes (http://windows.github.com/) or just "
            infoMsg += "download the latest snapshot from "
            infoMsg += "https://github.com/Xyntax/POC-T/archive/master.zip"
        else:
            infoMsg = "for Linux platform it's required "
            infoMsg += "to install a standard 'git' package (e.g.: 'sudo apt-get install git')"

        logger.info(infoMsg)

    sys.exit(0)
