from datetime import datetime
import re
#
import requests
from bs4 import BeautifulSoup

import csv


def getIntegerFromString(arg):
    if (arg == ' '):
        return 0
    return int(''.join(re.findall("\\d+", arg)))


def getMSDHpage():
    URL = 'https://msdh.ms.gov/msdhsite/_static/14,0,420.html'
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser')


def getMSDHdate():
    soup = getMSDHpage()
    raw_totals_date = soup.find(
        id='assetNow_pageSubtitle').text.split('Updated ')[1]
    updated_strp = datetime.strptime(raw_totals_date, '%B %d, %Y')
    updated_on = updated_strp.strftime('%Y-%m-%d')

    return updated_on


def getMississippiCounties():
    with open("counties.csv") as f:
        return [line.rstrip() for line in f]


def writeToCSV(outputName, updated_on, counties_totals):
    with open(
        "data/" +
        outputName +
        "_" +
        updated_on +
        ".csv", "w", newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerows(counties_totals)


def printArray(arr):
    for row in arr:
        print(row)
