#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# -----------------------------------------------------
#  FileName:    forms.py
#  Author  :    liuxing2@
#  Project :    fileserver.download
#  Date    :    2014-05-28 14:07
#  Descrip :    download object form
# -----------------------------------------------------

from django import forms
from download.models import DownloadFileModel

class DownloadFileForm(forms.ModelForm):
    """
    use:
        handle download form submit from client
    """

    filemd5 = forms.CharField(required=False)
    path = forms.CharField()
    lang = forms.CharField(required=False)
    params = forms.CharField(required=False)

    class Meta:
        model = DownloadFileModel
        fields = []	