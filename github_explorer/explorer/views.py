# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt

import csv
import json
import pandas as pd

import sqlite3

from datetime import datetime

@csrf_exempt
def index(request):
    languages = getLangs()

    if request.method == 'POST':

        language = request.POST['language']
        template = loader.get_template('explorer/base.html')

        color_list = ['#E91E63', '#9C27B0', '#673AB7', '#3F51B5',
            '#2196F3', '#FFC107', '#FF5722', '#03A9F4', '#00BCD4',
            '#8BC34A']
        bcolor_list = ['#EC407A', '#AB47BC', '#7E57C2', '#5C6BC0',
            '#42A5F5', '#FFCA28', '#FF7043', '#29B6F6', '#26C6DA',
            '#9CCC65']

        for lang in languages:
            if lang[0] == language:
                lang[1] = 'selected'

        d = getCounts(language)[language]
        piechart = loader.get_template('explorer/doughnutchart.html')
        piecontext = {'chartid': 'chart1', 'labels': ['Female', 'Male'],
            'data': d, 'colors': color_list[0:len(d)], 'hcolors': color_list[0:len(d)],
            'charttitle': 'Gender ratio for ' + language}
        piepiece = piechart.render(piecontext)
        context = {'charts': [[piepiece]], 'languages': languages}
        #return render(request, 'explorer/base.html', context)

        startyear = request.POST['start_year']
        endyear = request.POST['end_year']
        if startyear != '' and endyear != '':
            ystart = datetime.strptime(startyear, '%Y')
            yend = datetime.strptime(endyear, '%Y')
            cs = getContributorsOverTime(ystart, yend)['ContributorsOverTime']
            piechart2 = loader.get_template('explorer/doughnutchart.html')
            piecontext2 = {'chartid': 'chart2', 'labels': ['Female', 'Male'],
                'data': cs, 'colors': color_list[0:len(cs)], 'hcolors': color_list[0:len(cs)],
                'charttitle': 'Gender ratio from ' + startyear + 'to' + endyear}
            piepiece2 = piechart2.render(piecontext2)
            context['charts'][0].append(piepiece2)
            context['starty'] = startyear
            context['endy'] = endyear

        return render(request, 'explorer/base.html', context)


    context = {'languages': languages}

    return render(request, 'explorer/base.html', context)


def getCounts(language):
    file = os.path.join(settings.BASE_DIR, 'github.csv')
    datFrame =  pd.read_csv(file, sep=';')
    df = datFrame[datFrame['language'] == language]
    df = df[["language","genders"]]
    d = {}

    for index, row in df.iterrows():
        totalfCount = []
        totalmCount = []
        language = row['language']
        genders = row['genders']
        genderArray = genders.split()
        for gender in genderArray:
            fCount = gender.count("female")
            totalfCount.append(fCount)
            mCount = gender.count("male")
            totalmCount.append(mCount)

            if language in d:
                femaleCount,maleCount = d.get(language)
                newMaleCount = maleCount + totalmCount[0]
                newFemaleCount = femaleCount + totalfCount[0]
                d.update({language: (newFemaleCount, newMaleCount)})
            else:
                d.update({language: (totalfCount[0], totalmCount[0])} )

    print(d)
    return d


def getContributorsOverTime(startTime, endTime):
    file = os.path.join(settings.BASE_DIR, 'github.csv')
    datFrame = pd.read_csv(file, sep=';')
    dfTimeStamp = pd.to_datetime(datFrame['created_at'])
    datFrame['creationTime'] = dfTimeStamp;
    df = datFrame[(datFrame['creationTime'] >= startTime) & (datFrame['creationTime'] <= endTime )]
    df = df[["genders"]]
    d = {}

    totalfCount = []
    totalmCount = []
    for index, row in df.iterrows():
        genders = row['genders']
        genderArray = genders.split()
        for gender in genderArray:
            fCount = gender.count("female")
            totalfCount.append(fCount)
            mCount = gender.count("male")
            totalmCount.append(mCount)

            d.update({"ContributorsOverTime": (sum(totalfCount), sum(totalmCount))})

    return d


def getLangs():
    return [['Perl', ''], ['Objective-C', '']]


def getNations():
    return [['united states', ''], ['australia', '']]


# Create your views here.
