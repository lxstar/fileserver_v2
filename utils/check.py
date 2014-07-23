#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    check.py
#  Author  :    liuxing2@
#  Project :    utils.check
#  Date    :    2014-05-19 13:35
#  Descrip :    utils.check
# -----------------------------------------------------
from utils.get import get_decode_base64_str,get_file_md5,get_file_type,get_client_ip
from config import globalconf

def upload_check_params(model, path, request):
    """
    use:
        check client upload file params
    params:
        model: create from form
        path: dst path(like 'waf/5/192.168.1.1-aaaa-bbbb-cccc-dddd/test_waflog_2014_05.zip')
        request: index view request
    """
    result_code = ''
    path_list = get_decode_base64_str(path).split('/')
    file_md5 = get_file_md5(model.file)

    if not check_path(path_list):
        # path error
        result_code = '1003' 
    elif not check_md5(model.filemd5.upper(), file_md5):
        # file md5 different
        result_code = '1004' 
    elif not check_file_size(model.file.size):
        # file size more than globalconf.MAX_FILE_SIZE
        result_code = '1001' 
    elif not check_file_ext(model.file.name):
        # file ext not in globalconf.ALLOW_FILE_EXTS
        result_code = '1007'
    else:
        model.devtype = path_list[0]
        model.devhash = path_list[2][path_list[2].index('-') + 1:].upper()
        model.deversion = path_list[1]
        model.devip = path_list[2].split('-')[0]
        model.filename = path_list[-1]
        model.filemd5 = file_md5.upper()
        model.filetype = get_file_type(model.filename)
        model.clientip = get_client_ip(request)
        model.file.field.upload_to = "/".join((model.filetype, globalconf.DEFAULT_FILE_PATH))

        # normal result code
        result_code = '1000'
    return result_code, model

def check_file_size(size):
    """
    use:
        check file size is or not more than conf.MAX_FILE_SIZE
    params:
        size: file size
    return:
        True: size < globalconf.MAX_FILE_SIZE
        False: size > globalconf.MAX_FILE_SIZE
    """
    if size > globalconf.MAX_FILE_SIZE:
        return False
    else:
        return True

def check_file_ext(filename):
    """
    use:
        check file ext is or not in globalconf.ALLOW_FILE_EXTS
    params:
        filename
    return:
        True: file's ext is in globalconf.ALLOW_FILE_EXTS
        False: file's ext isn't in globalconf.ALLOW_FILE_EXTS
    """
    ext = filename.split('.')[-1]
    if ext in globalconf.ALLOW_FILE_EXTS:
        return True
    else:
        return False

def check_path(path_list):
    """
    use:
        check dst path
        (normal example: 'waf/5/192.168.1.1-aaaa-bbbb-cccc-dddd/test_waflog_2014_05.zip')
    params:
        path_list: path.split('/')
    return:
        True: path is normal
        False: path is abnormal
    """
    if len(path_list) == 4: 
        return True
    else:
        return False

def check_md5(md5_1, md5_2):
    """
    use: 
        check the two md5 values are same or not
    params:
        md5_1, md5_2: the two md5 values
    return:
        True: same
        False: different
    """

    if md5_1 and md5_2:
        if not cmp(md5_1, md5_2):
            return True
        else:
            return False
    else:
         return False

def check_file_path(filepath):
    """
    use:
        check file path is or isn't in globalconf.ALLOW_SAVE_PATHS
    params:
        filepath: file real path
    return:
        True or False
    """
    if filepath:
        for start in globalconf.ALLOW_SAVE_PATHS:
            if filepath.startswith(start):
                return True
    return False