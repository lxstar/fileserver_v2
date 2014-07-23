#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    views.py
#  Author  :    liuxing2@
#  Project :    fileserver.download
#  Date    :    2014-05-28 14:07
#  Descrip :    download app's views
# -----------------------------------------------------
from config import globalconf
import base64
import logging
import traceback

logger = logging.getLogger('plugins')

def upload_plugins_run(dev_info, file_info, params):
    """
    use:
        run upload plugins in globalconf.INSTALL_UPLOAD_PLUGINS
    params:
        dev_info: dev info from model
        file_info: file info from model
    return:
        None
    """
    plugin = None
    plugin_model = None

    for plugin_name in globalconf.INSTALL_UPLOAD_PLUGINS:
        try:
            plugin_model = __import__("".join(('plugins.upload.', plugin_name)), fromlist=[plugin_name])
            plugin = plugin_model.Plugin(dev_info, file_info, params)
            if plugin.is_run():
                plugin.run()
        except:
            logger.error('fileserver upload plugin run error, plugin name=%s'%plugin_name)
            logger.error(traceback.format_exc())

def download_plugins_run(dstpath, params):
    """
    use:
        run download plugins in globalconf.INSTALL_DOWNLOAD_PLUGINS
    params:
        dstpath: path from form(base64)
    return:
        None
    """
    plugin = None
    plugin_model = None
    params = {
        'result': '',
        'path': ''
    }

    for plugin_name in globalconf.INSTALL_DOWNLOAD_PLUGINS:
        try:
            plugin_model = __import__("".join(('plugins.download.', plugin_name)), fromlist=[plugin_name])
            plugin = plugin_model.Plugin(dstpath, params)
            if plugin.is_run():
                params = plugin.run()
                return params
        except:
            logger.error('fileserver download plugin run error, plugin name=%s'%plugin_name)
            logger.error(traceback.format_exc())
    return params

def search_plugins_run(dstpath, filemd5, params):
    """
    use:
        run search plugins in globalconf.INSTALL_SEARCH_PLUGINS
    params:
        dstpath: path from form
    return:
        None
    """
    plugin = None
    plugin_model = None
    filemd5 = ''

    for plugin_name in globalconf.INSTALL_SEARCH_PLUGINS:
        try:
            plugin_model = __import__("".join(('plugins.search.', plugin_name)), fromlist=[plugin_name])
            plugin = plugin_model.Plugin(dstpath, filemd5, params)
            if plugin.is_run():
                filemd5 = plugin.run()
                return filemd5
        except:
            logger.error('fileserver search plugin run error, plugin name=%s'%plugin_name)
            logger.error(traceback.format_exc())
    return filemd5