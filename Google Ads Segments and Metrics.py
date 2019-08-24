"""
https://developers.google.com/google-ads/api/fields/v2/segments
https://developers.google.com/google-ads/api/fields/v2/metrics
"""

from bs4 import BeautifulSoup
import requests as rq
import re
import csv
import string

##############
#Find Segments
##############

content = rq.get('https://developers.google.com/google-ads/api/fields/v2/segments').content
soup = BeautifulSoup(content, 'lxml')

name_tags = soup.find_all('h3')
description_tags = soup.find_all('td', {'class': "description"})

names = [name.text for name in name_tags if name.text.split('.')[0] == 'segments']
descriptions = [description.text for description in description_tags]

segment_dict = {}
for i in range(len(names)):
    segment_dict[names[i]] = descriptions[i]

with open('Google Ads Segments.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator = '\n', delimiter = ',')
    writer.writerow(['FieldName', 'FieldDescription','\n'])
    for key, value in segment_dict.items():
        writer.writerow([key, value])


#############
#Find Metrics
#############

content = rq.get('https://developers.google.com/google-ads/api/fields/v2/metrics').content
soup = BeautifulSoup(content, 'lxml')

name_tags = soup.find_all('h3')
description_tags = soup.find_all('td', {'class': "description"})

names = [name.text for name in name_tags if name.text.split('.')[0] == 'metrics']
descriptions = [description.text for description in description_tags]

metrics_dict = {}
for i in range(len(names)):
    metrics_dict[names[i]] = descriptions[i]

with open('Google Ads Metrics.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator = '\n', delimiter = ',')
    writer.writerow(['FieldName', 'FieldDescription','\n'])
    for key, value in metrics_dict.items():
        writer.writerow([key, value])
