import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://msdh.ms.gov/msdhsite/_static/14,0,420.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

cases = soup.find_all(class_="simpleTable")[-1]


tests = cases.find_all('tr')

msdh_total_tests_raw = tests[0].find_all('td')[1].text.split(',')
msdh_total_tests = int(''.join(msdh_total_tests_raw))


commercial_tests_raw = tests[1].find_all('td')[1].text.split(',')
commercial_tests = int(''.join(commercial_tests_raw))

testing = [msdh_total_tests, commercial_tests, msdh_total_tests+commercial_tests]

print(testing)

# Write to csv
with open("covid_tests.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(map(lambda x: [x], testing))