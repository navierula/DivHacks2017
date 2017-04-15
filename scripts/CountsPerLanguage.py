import csv
import json
import pandas as pd

file = "/Users/ravielakshmanan/Downloads/diversity/diversity_data.csv"
datFrame = pd.read_csv(file, sep=';')
dfTimeStamp = pd.to_datetime(datFrame['created_at'])
datFrame['creationTime'] = dfTimeStamp;

def getCounts(language):
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
    return d

def getContributorsOverTime(startTime, endTime):
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

def main():
    l = getCounts("Perl")
    d = getContributorsOverTime("2012-11-23 17:26:24", "2012-11-23 17:26:26")
    print(l)
    print(d)

if __name__== "__main__":
  main()