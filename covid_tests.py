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


print(msdh_total_tests)

test_counts = []


"""
# Write to csv
with open("out_tests.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(counties_totals)
"""