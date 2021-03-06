#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 18:13:31 2017

@author: navrajnarula
"""


import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np
from collections import Counter

# read in dataset
df = pd.read_csv("data_sources/GitHub_Terms_Data.csv", sep=';', encoding='ISO-8859-1')

list(df.columns.values)

# returns number of male and female contributors
# in a tuple
def contribution_by_gender(df):
    genderList = []
    for val in df["genders"]:
        genderList.append(val)

    totalfCount = []
    totalmCount = [] 
    
    for gender in genderList:
        fCount = gender.count("female")
        totalfCount.append(fCount)
        mCount = gender.count("male")
        totalmCount.append(mCount)
    
    return (sum(totalmCount), sum(totalfCount))

# returns dictionary of programming languages
# and number of times males vs. female used
# those languages
def languages_by_gender(df):
    languages = {}
    for valOne, valTwo in zip(df["language"], df["genders"]):     
        try:
            languages[valOne].append(valTwo)
        except KeyError:
            languages[valOne] = [valTwo]

    maleCount = 0
    femaleCount = 0
    for key, val in languages.items():
        for item in val:
            if "male" in item:
                maleCount +=1
            if "female" in item:
                femaleCount += 1
    languages[key] = (maleCount, femaleCount)
    
    return languages

# returns a list of all languages used 
def language_list(df):
    languages = []
    for val in df["language"]:
        languages.append(val)
    return sorted(list(set(languages)))

# returns dict_items of countributions by country in numbers
def contributions_by_country(df):
    countries_list = []
    for val in df["countries"]:
        splits = val.split(",")
        countries_list.append(splits)
    entire_list = [item for sublist in countries_list for item in sublist if item != "None"]
    c = Counter(entire_list)
    return c.items()

# returns list of countries in alphabetical order
def countries_list(df):
    countries_list = []
    for val in df["countries"]:
        splits = val.split(",")
        countries_list.append(splits)
    entire_list = [item for sublist in countries_list for item in sublist if item != "None"]
    entire_list = list(set(entire_list))
    return sorted(entire_list)
    
    

    

    

