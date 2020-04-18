import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://msdh.ms.gov/msdhsite/_static/14,0,420.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

cases = soup.find(id='msdhTotalCovid-19Cases')

counties = cases.find_all('tr')

counties_totals = []

for county in counties:
    data = county.find_all('td')
    county_name = data[0].text
    if (county_name != 'County' and county_name != 'Total'):
        county_cases = data[1].text

        county_deaths = data[2].text
        if (county_deaths == ' '):
            county_deaths = 0
        county_ltcs = data[3].text
        if (county_ltcs == ' '):
            county_ltcs = 0
        # print(county_name, ':', int(county_cases), '|',
        #       int(county_deaths), '|', int(county_ltcs))
        county_data = [county_name, int(county_cases), int(
            county_deaths), int(county_ltcs)]
        counties_totals.append(county_data)

# Extremely janky code to test if issaquena if it's still at 0 cases
# and if so, add it

# Set default that issaquena is still 0
issaquena_test = False

# test each county to check
for row in counties_totals:
    print(row[0])
    # if issaquena exists, set to tru
    if (row[0] == 'Issaquena'):
        issaquena_test = True

# if it still doesn't add it and sort list
if(issaquena_test == False):
    counties_totals.append(['Issaquena', 0, 0, 0])
    counties_totals.sort(key=lambda x: x[0])

print(counties_totals)

# Write to csv
with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(counties_totals)
