# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader

def index(request):
    template = loader.get_template('explorer/base.html')
    context = {}
    return render(request, 'explorer/base.html', context)

# Create your views here.
