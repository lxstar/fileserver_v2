#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    get.py
#  Author  :    liuxing2@
#  Project :    utils.get
#  Date    :    2014-05-19 13:35
#  Descrip :    utils.get
# -----------------------------------------------------
from upload.models import UploadFileModel
from config import globalconf
from hashlib import md5
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import os
import base64
import logging
import traceback

logger = logging.getLogger('download')

def get_client_ip(request):
    """
    use: 
        get client ip from request
    params:
        request: the request from view
    return:
        client ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_file_md5_search(dstpath, filemd5=None):
    """
    use:
        get file md5 from database with dstpath or filemd5
        also make sure the file is exist
        if dstpath and filemd both have:
            filemd5 worked
    params:
        dstpath: the path from client path params
                 not filepath in fileserver nfs !!!
        filemd5: file's md5 from client
    return:
        db_file_md5: can find in database
        None: can not find in database
    """
    upload_obj = None

    if filemd5:
        upload_obj = UploadFileModel.objects.filter(filemd5=filemd5).only('id', 'filemd5', 'file').order_by('-id')
    else:
        upload_obj = UploadFileModel.objects.filter(path=dstpath).only('id', 'file', 'filemd5').order_by('-id')
    
    if upload_obj:
        if os.path.isfile(os.path.join(globalconf.FILESERVER_SAVE_PATH, str(upload_obj[0].file))):
            return upload_obj[0].filemd5
    else:
        return ''

def get_file_md5(fp):
    """
    use: 
        get file md5 
    params:
        fp: file object, such as fp = open('...', '...')
    return:
        file md5 upper
    """
    md5_obj = md5()
    md5_obj.update(fp.read())
    return md5_obj.hexdigest().upper()

def get_error_lang(form):
    """
    use: 
        get language for error's messages
        define in globalconf.ERRORS's key
    params: 
        form: upload file form from brower
    return:
        user lang: if the choice lang we have
        default lang: we have not this language
                      define at globalconf.DEFAULT_ERROR_LANG
    """
    if form.cleaned_data['lang'] in globalconf.ERRORS:
        return form.cleaned_data['lang']
    else:
        return globalconf.DEFAULT_ERROR_LANG

def get_error_info(lang, result_code):
    """
    use: 
        get error msgs by lang and result code(globalconf.ERRORS)
    params: 
        lang: error language
        result_code: error code
    return:
        error_info: the error info
    """
    if lang not in globalconf.ERRORS:
        lang = globalconf.DEFAULT
    errors = globalconf.ERRORS[lang]
    error_info = {
        'result': result_code,
        'msgs': errors[result_code]    
    }
    return error_info

def get_decode_base64_str(base64_str):
    """
    use: 
        decode base64 string
    params: 
        base64_str: base64 string
    return:
        "": base64 string error
        string: decode string
    """
    if base64_str:
        try:
            decode_str = base64.decodestring(base64_str)
            return decode_str
        except:
            return "" 
    else:
        return ""

def get_file_type(filename):
    """
    use:
        get filetype from filename
    params:
        filename: such as 'xxx_filetype_xxx_xx_xx.xxx'
                  two '_' must, if not filetype='other'
    return:
        filetype
    """
    filename_list = filename.split('_')
    if len(filename_list) > 2:
        return filename_list[1]
    else:
        return globalconf.DEFAULT_FILE_TYPE

def get_dev_file_info(model):
    """
    use:
        get dev_info and file_info from model
    params:
        upload model include dev and file infos
    return dev_info, file_info
    """
    dev_info = {}
    file_info = {}

    if model:

        dev_info = {
            'devtype': model.devtype,
            'devhash': model.devhash,
            'devip': model.devip,
            'deversion': model.deversion
        }

        file_info = {
            'filename': model.filename,
            'filetype': model.filetype,
            'filepath': model.file.path.replace(globalconf.FILESERVER_SAVE_PATH, '')
        }
    return dev_info, file_info

def get_file_path_and_filename(dstpath, filemd5=None):
    """
    use:
        get file real path from database with dstpath or filemd5
        if dstpath and filemd both have:
            filemd5 worked
    params:
        dstpath: the path from client path params
                 not filepath in fileserver nfs !!!
        filemd5: file's md5 from client
    return:
        realpath: can find in database
        None: can not find in database
    """
    upload_obj = None

    if filemd5:
        upload_obj = UploadFileModel.objects.filter(filemd5=filemd5).only('id', 'filemd5', 'file', 'filename').order_by('-id')
    else:
        upload_obj = UploadFileModel.objects.filter(path=dstpath).only('id', 'file', 'filename').order_by('-id')
    if upload_obj:
        return os.path.join(globalconf.FILESERVER_SAVE_PATH, str(upload_obj[0].file)), upload_obj[0].filename
    else:
        return None, None

def get_file_response(filepath, filename):
    """
    use:
        get HttpResponse object for download file streaming
    params:
        filepath: file real path on fileserver
    return:
        FileHttpResponse: realpath right and file is exist
        None: realpath failed or file isn't exist
    """
    if not filename and filepath:
        filename = filepath.split('/')[-1]

    if filepath and os.path.isfile(str(filepath)):
        try:
            data = FileWrapper(file(filepath))
        except:
            logger.error('download read file error.')
            logger.error(traceback.format_exc())

        response = HttpResponse(data)
        response['mimetype'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=%s'%filename
        response['Content-Length'] = os.path.getsize(filepath)

        return response
    else:
        return None