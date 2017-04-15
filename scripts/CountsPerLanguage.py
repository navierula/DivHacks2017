import csv
import json
import pandas as pd

def getCounts(language):
    file = "/Users/ravielakshmanan/Downloads/diversity/diversity_data.csv"
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

def main():
    getCounts("Perl")

if __name__== "__main__":
  main()