#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    urls.py
#  Author  :    liuxing2@
#  Project :    fileserver.fileserver
#  Date    :    2014-05-28 14:07
#  Descrip :    the base urls for fileserver project
# -----------------------------------------------------

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
            (r'^upload/', include('upload.urls')),
            (r'^download/', include('download.urls')),
            (r'^search/', include('search.urls'))
)
