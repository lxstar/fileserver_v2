#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    fileserver.download
#  Date    :    2014-05-28 14:07
#  Descrip :    download app's views
# -----------------------------------------------------

from django.http import HttpResponse
from download.forms import DownloadFileForm
from config import globalconf
from utils.get import get_client_ip, get_error_lang, get_file_path_and_filename,\
                     get_file_response,get_error_lang,get_error_info,\
                     get_decode_base64_str
from utils.check import check_file_path
from plugins.run import download_plugins_run

import json
import os
import logging

# logger named 'download'
# define in logging.cfg's [logger_download]
logger = logging.getLogger('download')

def index(request):
    """
    use:
        return index download view
    params:
        request: the request from client
    return:
        HttpResponse: the file download 
    """
    error_lang = globalconf.DEFAULT_ERROR_LANG
    result_code = ''
    file_response = None

    form = DownloadFileForm(request.REQUEST)

    if form.is_valid():
        error_lang = get_error_lang(form)
        
        filename = ""
        dstpath = form.cleaned_data['path']
        base64_de_dstpath = get_decode_base64_str(dstpath)
        params = form.cleaned_data['params']
        filemd5 = form.cleaned_data['filemd5'].upper()

        if base64_de_dstpath:
            plugin_params = download_plugins_run(base64_de_dstpath, params)
        else:
            plugin_params = {}

        filepath =  plugin_params.get('path', '')

        if not filepath:
            filepath, filename = get_file_path_and_filename(dstpath, filemd5)
            
        if filepath and os.path.isfile(str(filepath)) \
                    and check_file_path(str(filepath)):
            file_response = get_file_response(filepath, filename)

        if file_response:
            model = form.save(commit=False)
            model.clientip = get_client_ip(request)
            model.filepath = filepath
            model.save()
        else:
            # '1002': 'file is not exist'
            if  plugin_params.get('result' ,''):
                result_code =   plugin_params.get('result')
            else:
                result_code = '1002'                
    else:
        # '1008': 'upload form insufficient parameters'
        result_code = '1008'

    if file_response:
        return file_response
    else:
        return  HttpResponse(json.dumps(get_error_info(error_lang, result_code)))