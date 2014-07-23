#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    creditdownload.py
#  Author  :    lihonglei
#  Project :    fileserver.plugins
#  Date    :    2014-06-11 14:07
#  Descrip :    download plugin template
# -----------------------------------------------------
from config import globalconf as conf

import logging
from utils.mysqlconnection import MySQLConnect

logger = logging.getLogger('plugins')

"""
credit download plugin

"""

mysql = MySQLConnect(host=conf.CREDIT_MYSQL_HOST,port=conf.CREDIT_MYSQL_PORT,user=conf.CREDIT_MYSQL_USER,
                   passwd=conf.CREDIT_MYSQL_PASSWORD,dbname=conf.CREDIT_MYSQL_DBNAME )
SELECT_MAXVERSION = "select max(file_version) from credit_files"
SELECT_CREDITFILE = "select file_path from credit_files where file_version=%s"

class Plugin(object):

    __name = "credit download plugin"
    __version = "0.1"

    def __init__(self, dstpath, params):
        self.dstpath = dstpath
        self.params = params

    def is_run(self):
        return 'credit' in self.dstpath

    def run(self):
        try:
            resVersion = mysql.execute(SELECT_MAXVERSION)
            maxVersion = resVersion[0][0]
            results = mysql.execute(SELECT_CREDITFILE,(maxVersion))
            fileName = results[0][0]

            pathList = self.dstpath.split('/')
            version = pathList[1]
            if version:
                if version == maxVersion:
                    fileName = None
        except Exception as e:
            logger.error('credit download error:%s',e)
        return { 'result':'1000' , 'path': fileName}
