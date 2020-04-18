import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

URL = 'https://msdh.ms.gov/msdhsite/_static/14,0,420.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

raw_totals_date = soup.find(
    id='assetNow_pageSubtitle').text.split('Updated ')[1]
updated_strp = datetime.strptime(raw_totals_date, '%B %d, %Y')
updated_on = updated_strp.strftime('%Y-%m-%d')

cases = soup.find(id='msdhTotalCovid-19Cases')

counties = cases.find_all('tr')

counties_totals = []

for county in counties:
    data = county.find_all('td')
    county_name = data[0].text
    if (county_name != 'County' and county_name != 'Total'):

        county_cases = data[1].text
        if (county_cases == ' '):
            county_cases = 0

        county_deaths = data[2].text
        if (county_deaths == ' '):
            county_deaths = 0

        county_ltcs = data[3].text
        if (county_ltcs == ' '):
            county_ltcs = 0

        county_data = [updated_on, county_name, int(county_cases), int(
            county_deaths), int(county_ltcs)]
        counties_totals.append(county_data)

# Imports list of counties
with open("counties.csv") as f:
    counties_list = [line.rstrip() for line in f]

# Loops through the list to see if it exists in the scraped data.
# If it doesn't... add it with 0 totals
for county_element in counties_list:
    is_found = any(county_element in sublist for sublist in counties_totals)
    if(is_found == False):
        counties_totals.append([updated_on, county_element, 0, 0, 0])

# Sort the list due to any added counties
counties_totals.sort(key=lambda x: x[1])
# print(counties_totals)

# Write to csv
with open("covid_totals_"+updated_on+".csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(counties_totals)
