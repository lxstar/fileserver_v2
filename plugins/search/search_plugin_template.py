#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    search_plugin_template.py
#  Author  :    liuxing2@
#  Project :    fileserver.plugins
#  Date    :    2014-05-28 14:07
#  Descrip :    search plugin template
# -----------------------------------------------------

import logging
logger = logging.getLogger('plugins')

"""
search plugin template

1. class name must be 'Plugin'
2. function is_run and run must
"""


class Plugin(object):

    __name = "search plugin template"
    __version = "0.1"

    def __init__(self, dstpath, filemd5, params):
        self.dstpath = dstpath
        self.filemd5 = filemd5
        self.params = params

    def is_run(self):
        
        logger.debug('upload template is_run function')
        if self.params == 'nsfocus':
            return True
        else:
            return False

    def run(self):

        logger.debug('upload template run function')
        filemd5 = "test_file_md5"
        return filemd5
