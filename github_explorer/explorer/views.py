# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.conf import settings
import os

import sqlite3

def index(request):
    template = loader.get_template('explorer/base.html')
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'github.db'))
    d = conn.execute('select count(*) from github')
    l = []
    for d1 in d:
        l.append(d1)
    w = conn.execute('select count(*) from github where has_woman=\'True\'')
    lw = []
    for w1 in w:
        lw.append(w1)
    men_cnt = l[0][0] - lw[0][0]
    women_cnt = lw[0][0]
    #context = {'test': l[0][0], 'men_cnt': men_cnt, 'women_cnt': women_cnt}
    conn.close()

    charttemplate = loader.get_template('explorer/doughnutchart.html')
    charts = []
    for i in range(0, 4):
        chartcontext = {'chartid': 'chart' + str(i), 'charttitle': 'Gender ratio', 'labels': ['Male', 'Female'], 'data': [men_cnt, women_cnt], 'colors': ["#FF6384", "#36A2EB"], 'hcolors': ["#FF6384", "#36A2EB"]}
        chartrender = charttemplate.render(chartcontext)
        charts.append(chartrender)
    context = {'charts': charts}

    return render(request, 'explorer/base.html', context)

# Create your views here.
