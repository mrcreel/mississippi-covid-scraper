import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from functions import getIntegerFromString, getMSDHpage

soup = getMSDHpage()

"""
URL = 'https://msdh.ms.gov/msdhsite/_static/14,0,420.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
"""
raw_totals_date = soup.find(
    id='assetNow_pageSubtitle').text.split('Updated ')[1]
updated_strp = datetime.strptime(raw_totals_date, '%B %d, %Y')
updated_on = updated_strp.strftime('%Y-%m-%d')

cases = soup.find(id='msdhTotalCovid-19CasesByRace')

counties = cases.find_all('tr')

counties_totals = []

for county in counties:
    data = county.find_all('td')
    county_name = data[0].text
    if (county_name != 'County' and county_name != 'Total'):

        county_cases = data[1].text
        if (county_cases == ' '):
            county_cases = 0

        county_black = data[2].text
        if (county_black == ' '):
            county_black = 0

        county_white = data[3].text
        if (county_white == ' '):
            county_white = 0

        county_other = data[4].text
        if (county_other == ' '):
            county_other = 0

        county_unknown = data[5].text
        if (county_unknown == ' '):
            county_unknown = 0

        county_data = [updated_on, county_name, int(county_cases), int(
            county_black), int(county_white), int(county_other), int(county_unknown)]
        counties_totals.append(county_data)

# Imports list of counties
with open("counties.csv") as f:
    counties_list = [line.rstrip() for line in f]

# Loops through the list to see if it exists in the scraped data.
# If it doesn't... add it with 0 totals
for county_element in counties_list:
    is_found = any(county_element in sublist for sublist in counties_totals)
    if(is_found == False):
        counties_totals.append([updated_on, county_element, 0, 0, 0, 0, 0])

# Sort the list due to any added counties
counties_totals.sort(key=lambda x: x[1])
print(counties_totals)
"""
# Write to csv
with open("data/covid_racial_"+updated_on+".csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(counties_totals)
"""
