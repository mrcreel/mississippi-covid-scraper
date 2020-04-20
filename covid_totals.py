import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from functions import getIntegerFromString, getMSDHpage, getMSDHdate, getMississippiCounties, writeToCSV, printArray

outputName = 'covid_totals'

soup = getMSDHpage()

updated_on = getMSDHdate()

cases = soup.find(id='msdhTotalCovid-19Cases')

counties = cases.find_all('tr')

counties_totals = []

for county in counties:
    data = county.find_all('td')
    county_name = data[0].text
    if (county_name != 'County' and county_name != 'Total'):

        county_cases = getIntegerFromString(data[1].text)
        county_deaths = getIntegerFromString(data[2].text)
        county_ltcs = getIntegerFromString(data[3].text)

        counties_totals.append(
            [
                updated_on,
                county_name,
                county_cases,
                county_deaths,
                county_ltcs
            ]
        )

# Loops through the list to see if it exists in the scraped data.
# If it doesn't... add it with 0 totals
for county_element in getMississippiCounties():
    is_found = any(county_element in sublist for sublist in counties_totals)
    if(is_found == False):
        counties_totals.append([updated_on, county_element, 0, 0, 0])

# Sort the list due to any added counties
counties_totals.sort(key=lambda x: x[1])
print(printArray(counties_totals))


writeToCSV(outputName, updated_on, counties_totals)
