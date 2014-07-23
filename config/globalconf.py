#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    globalconf.py
#  Author  :    liuxing2@
#  Project :    fileserver.fileserver
#  Date    :    2014-05-28 14:07
#  Descrip :    configuration for fileserver project
# -----------------------------------------------------

# mysql database conf
FILESERVER_MYSQL_DB_NAME = ''
FILESERVER_MYSQL_DB_USER = ''
FILESERVER_MYSQL_DB_PWD = ''
FILESERVER_MYSQL_DB_HOST = ''
FILESERVER_MYSQL_DB_PORT = ''

# fileserver file path
FILESERVER_SAVE_PATH = ''

# uplaod plugins install
INSTALL_UPLOAD_PLUGINS = []

# download plugins install
INSTALL_DOWNLOAD_PLUGINS = ['creditdownload',]

# search plugins install
INSTALL_SEARCH_PLUGINS = ['creditsearch',]

# errors define
ERRORS = {
    'en': {
        '1000': 'normal',
        '1001': 'file size exceeds limit',
        '1002': 'file is not exist',
        '1003': 'file path error',
        '1004': 'file md5 error',
        '1005': 'language error',
        '1006': 'request method error, must be POST',
        '1007': 'file ext not allow',
        '1008': 'form insufficient parameters',
        '1404': 'unknown error',
    },
    'cn': {
        '1000': '正常返回值',
        '1001': '文件大小超过上限',
        '1002': '文件不存在',
        '1003': '文件目标路径错误',
        '1004': '文件MD5值不一致',
        '1005': '返回值语言不存在',
        '1006': '请求类型错误，必须是POST',
        '1007': '文件类型不允许',
        '1008': '表单参数不足',
        '1404': '未知错误',
    }
}

# default error language
DEFAULT_ERROR_LANG = 'en'

# max size limit 
MAX_FILE_SIZE = 104857600 # 100MB 

# allow file ext
ALLOW_FILE_EXTS = ['zip', 'tar', 'gz', 'rar'] 

# default filetype
DEFAULT_FILE_TYPE = "other"

# default file save path
DEFAULT_FILE_PATH = "%Y/%m/%d/%H/%M/%S"

# redis conf
REDIS_HOST = ''
REDIS_PORT = ''

# allow save file path
ALLOW_SAVE_PATHS = [
    FILESERVER_SAVE_PATH,
    '/opt/disk2/chroot/nfs/credit/',
]

# settings debug
DEBUG = False


#credit database
CREDIT_MYSQL_HOST = ''
CREDIT_MYSQL_PORT = 
CREDIT_MYSQL_DBNAME = ''
CREDIT_MYSQL_USER = ''
CREDIT_MYSQL_PASSWORD = ''
CREDIT_MYSQL_TIMEOUT = 

FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600 * 2 # 200MB