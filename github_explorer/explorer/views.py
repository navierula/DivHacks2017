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

from collections import Counter


countries_begin = 0


@csrf_exempt
def index(request):
    languages = getLangs()
    nations = getNations()

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
            'data': d, 'colors': color_list[0:len(d)], 'hcolors': bcolor_list[0:len(d)],
            'charttitle': 'Gender ratio for ' + language}
        piepiece = piechart.render(piecontext)
        context = {'charts': [[piepiece]], 'languages': languages, 'nations': nations, 'is_gender': 1,
            'theme': 'Gender'}
        #return render(request, 'explorer/base.html', context)

        startyear = request.POST['start_year']
        endyear = request.POST['end_year']
        if startyear != '' and endyear != '':
            ystart = datetime.strptime(startyear, '%Y')
            yend = datetime.strptime(endyear, '%Y')
            cs = getContributorsOverTime(ystart, yend)['ContributorsOverTime']
            piechart2 = loader.get_template('explorer/doughnutchart.html')
            piecontext2 = {'chartid': 'chart2', 'labels': ['Female', 'Male'],
                'data': cs, 'colors': color_list[0:len(cs)], 'hcolors': bcolor_list[0:len(cs)],
                'charttitle': 'Gender ratio from ' + startyear + ' to ' + endyear}
            piepiece2 = piechart2.render(piecontext2)
            context['charts'][0].append(piepiece2)
            context['starty'] = startyear
            context['endy'] = endyear

        return render(request, 'explorer/base.html', context)


    context = {'languages': languages, 'nations': nations, 'is_gender': 1, 'theme': 'Gender'}

    return render(request, 'explorer/base.html', context)


@csrf_exempt
def countries(request):

    countries_begin = request.session.get('num')
    if countries_begin == None:
        countries_begin = request.session.get('num', 0)


    if request.method == 'GET':
        if 'action' in request.GET:
            if request.GET['action'] == '1':
                countries_begin += 10
            else:
                countries_begin -=10
                if countries_begin < 0:
                    countries_begin = 0

    request.session['num'] = countries_begin

    languages = getLangs()
    nations = getNations()

    #if request.method == 'POST':

    tnations = []
    for i in range(countries_begin, countries_begin + 10):
        tnations.append(nations[i][0])
    template = loader.get_template('explorer/base.html')

    color_list = ['#E91E63', '#9C27B0', '#673AB7', '#3F51B5',
        '#2196F3', '#FFC107', '#FF5722', '#03A9F4', '#00BCD4',
        '#8BC34A']
    bcolor_list = ['#EC407A', '#AB47BC', '#7E57C2', '#5C6BC0',
        '#42A5F5', '#FFCA28', '#FF7043', '#29B6F6', '#26C6DA',
        '#9CCC65']

    tcontribs = []
    contribs = contributions_by_country()
    for n in tnations:
        for x in contribs:
            if x[0] == n:
                tcontribs.append(x[1])
    barchart = loader.get_template('explorer/barchart.html')
    barcontext = {'chartid': 'chart1', 'labels': tnations,
        'data': tcontribs, 'colors': color_list[0:len(tcontribs)], 'hcolors': bcolor_list[0:len(tcontribs)],
        'charttitle': 'Contributions by nationaility', 'label': 'Nationality', 'is_gender': 0}
    barpiece = barchart.render(barcontext)
    context = {'charts': [[barpiece]], 'languages': languages, 'nations': nations, 'theme': 'Nationality'}
    #return render(request, 'explorer/base.html', context)

    return render(request, 'explorer/base.html', context)


    context = {'languages': languages, 'nations': nations}

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
    l = []
    file = os.path.join(settings.BASE_DIR, 'github.csv')
    datFrame = pd.read_csv(file, sep=';')
    ll = language_list(datFrame)
    for ll1 in ll:
        l.append([ll1, ''])
    return l


def language_list(df):
    languages = []
    for val in df["language"]:
        languages.append(val)
    return sorted(list(set(languages)))


def getNations():
    c = []
    file = os.path.join(settings.BASE_DIR, 'github.csv')
    datFrame = pd.read_csv(file, sep=';')
    cl = countries_list(datFrame)
    for cl1 in cl:
        c.append([cl1, ''])
    return c


def countries_list(df):
    countries_list = []
    for val in df["countries"]:
        splits = val.split(",")
        countries_list.append(splits)
    entire_list = [item for sublist in countries_list for item in sublist if item != "None"]
    entire_list = list(set(entire_list))
    return sorted(entire_list)


def contributions_by_country():
    file = os.path.join(settings.BASE_DIR, 'github.csv')
    df = pd.read_csv(file, sep=';')
    countries_list = []
    for val in df["countries"]:
        splits = val.split(",")
        countries_list.append(splits)
    entire_list = [item for sublist in countries_list for item in sublist if item != "None"]
    c = Counter(entire_list)
    return c.items()


# Create your views here.
