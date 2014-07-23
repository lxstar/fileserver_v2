#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    fileserver.search
#  Date    :    2014-05-28 14:07
#  Descrip :    fileserver.views
# -----------------------------------------------------

from django.http import HttpResponse
from config import globalconf
from search.forms import FindFileForm
from utils.get import get_error_lang, get_error_info,get_file_md5_search,get_decode_base64_str
from plugins.run import search_plugins_run

import logging
import json

# logger named 'search'
# define in logging.cfg's [logger_search]
logger = logging.getLogger('search')


def find_file(request):
    """
    use:
        fild file with md5 or path(not real path)
    params:
        request: views.request
    return:
        file streaming: find file right
        error_info: not find file
                    {
                        'result_code': (string),
                        'msgs': (string),
                        'filemd5': (file'md5 or ''),
                    }
    """
    error_lang = globalconf.DEFAULT_ERROR_LANG
    result_code = ''
    db_filemd5 = ''

    form = FindFileForm(request.REQUEST)
    if form.is_valid():
        error_lang = get_error_lang(form)

        dstpath = form.cleaned_data['path']
        base64_de_dstpath = get_decode_base64_str(dstpath)
        filemd5 = form.cleaned_data['filemd5'].upper()
        params = form.cleaned_data['params']
        if base64_de_dstpath:
            db_filemd5 = search_plugins_run(base64_de_dstpath, filemd5, params)
        else:
            db_filemd5 = ""
            
        if not db_filemd5:
            db_filemd5 = get_file_md5_search(dstpath, filemd5)

        if db_filemd5:
            result_code = '1000'
        else:
            result_code = '1002'
    else:
        # '1008': 'upload form insufficient parameters'
        result_code = '1008'  

    error_info = get_error_info(error_lang, result_code)
    error_info['filemd5'] = db_filemd5
    return HttpResponse(json.dumps(error_info)) 