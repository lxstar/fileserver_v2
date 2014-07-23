#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    creditsearch.py
#  Author  :    lihonglei
#  Project :    fileserver.plugins
#  Date    :    2014-06-20 11:07
#  Descrip :    credit search plugin
# -----------------------------------------------------

import logging
logger = logging.getLogger('plugins')
from config import globalconf as conf
from utils.mysqlconnection import MySQLConnect
"""
credit search plugin

"""

mysql = MySQLConnect(host=conf.CREDIT_MYSQL_HOST,port=conf.CREDIT_MYSQL_PORT,user=conf.CREDIT_MYSQL_USER,
                   passwd=conf.CREDIT_MYSQL_PASSWORD,dbname=conf.CREDIT_MYSQL_DBNAME )
SELECT_MAXVERSION = "select max(file_version) from credit_files"
SELECT_CREDITFILE = "select file_md5 from credit_files where file_version=%s"

class Plugin(object):

    __name = "credit search plugin"
    __version = "0.1"

    def __init__(self, dstpath, filemd5, params):
        self.dstpath = dstpath
        self.filemd5 = filemd5
        self.params = params

    def is_run(self):
        return 'credit' in self.dstpath

    def run(self):
        try:
            resVersion = mysql.execute(SELECT_MAXVERSION)
            maxVersion = resVersion[0][0]
            results = mysql.execute(SELECT_CREDITFILE,(maxVersion))
            fileMd5 = results[0][0]
        except Exception as e:
            logger.error('credit search error:%s',e)
        return fileMd5

