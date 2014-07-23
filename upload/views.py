#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    fileserver.upload
#  Date    :    2014-05-19 13:35
#  Descrip :    upload.views
# -----------------------------------------------------

from django.http import HttpResponse
from upload.forms import UploadFileForm
from config import globalconf
from utils.get import get_error_lang,get_error_info,get_dev_file_info
from utils.check import upload_check_params
from plugins.run import upload_plugins_run
import json

import logging

logger = logging.getLogger('upload')

def index(request):
    """
    use: 
        return index upload view
    params: 
        request: the request from client
    return:
        HttpResponse: the result for upload file (json)
    """
    error_lang = globalconf.DEFAULT_ERROR_LANG
    result_code = ''

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            path = form.cleaned_data['path']
            params = form.cleaned_data['params']
            error_lang = get_error_lang(form)

            result_code, model= upload_check_params(model, path, request)
            # '1000': 'normal'
            if result_code == '1000':

                dev_info, file_info = get_dev_file_info(model)
                upload_plugins_run(dev_info, file_info, params)
                model.save()

                logger.info('upload file success')
                logger.info('filename:%s client_ip:%s path:%s'%\
                            (model.filename, model.clientip, model.file.path))
        else:
            # '1008': 'upload form insufficient parameters'
            result_code = '1008'
    else:
        # '1006': 'request method error, must be POST'
        result_code = '1006'

    return HttpResponse(json.dumps(get_error_info(error_lang, result_code)))