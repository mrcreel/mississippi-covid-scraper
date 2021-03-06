import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = 'https://msdh.ms.gov/msdhsite/_static/14,0,420.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

raw_totals_date = soup.find(
    id='assetNow_pageSubtitle').text.split('Updated ')[1]
updated_strp = datetime.strptime(raw_totals_date, '%B %d, %Y')
updated_on = updated_strp.strftime('%Y-%m-%d')

cases = soup.find_all(class_="simpleTable")[-1]

tests = cases.find_all('tr')


msdh_total_tests_raw = tests[0].find_all('td')[1].text.split(',')
msdh_total_tests = int(''.join(msdh_total_tests_raw))

commercial_tests_raw = tests[1].find_all('td')[1].text.split(',')
commercial_tests = int(''.join(commercial_tests_raw))

uls = soup.find_all('ul')
mphl = uls[14]
mphl_data = mphl.find_all('li')
mphl_tests = mphl_data[0].text.split(': ')[1].split(',')
mphl_tests = int(''.join(mphl_tests))

testing = [updated_on, msdh_total_tests, commercial_tests,
           msdh_total_tests+commercial_tests, mphl_tests]

print(testing)

# Write to csv
with open("data/covid_tests_"+updated_on+".csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(testing)
