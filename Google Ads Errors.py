"""
https://developers.google.com/google-ads/api/reference/rpc/google.ads.googleads.v2.errors#accessinvitationerrorenum
"""

from bs4 import BeautifulSoup
import requests as rq
import re
import csv
import string


def remove_empty_spaces(lst):
    for i in lst:
        if i == '':
            lst.remove('')

def remove_fields_and_enums(lst):
    lst.remove('Index')
    lst.remove('ErrorCode')
    lst.remove('ErrorDetails')
    lst.remove('ErrorLocation')
    lst.remove('FieldPathElement')
    lst.remove('GoogleAdsError')
    lst.remove('GoogleAdsFailure')
    lst.remove('PolicyFindingDetails')
    lst.remove('PolicyViolationDetails')
    for word in lst:
        if word[-4::] == 'Enum':
            lst.remove(word)

def add_resource_name_to_field_new_dict(field_name_types):

    new_field_dict = {}
    for lst in field_name_types:
        if lst[0][-5::] == 'error' or lst[0] == 'unpublished_error_code' or lst[0] == 'policy_violation_details' or lst[0] == 'policy_finding_details':
            new_key = lst[0]
            new_resource_name = 'ErrorDetails'
            lst.append(new_resource_name)
            new_value = lst[1:]
            new_field_dict[new_key] = new_value

        elif lst[0] == 'field_path_elements[]':
            new_key = lst[0]
            new_resource_name = 'ErrorLocation'
            lst.append(new_resource_name)
            new_value = lst[1:]
            new_field_dict[new_key] = new_value

        elif lst[0] == 'field_name' or lst[0] == 'index':
            new_key = lst[0]
            new_resource_name = 'FieldPathElement'
            lst.append(new_resource_name)
            new_value = lst[1:]
            new_field_dict[new_key] = new_value

        elif lst[0] == 'error_code' or lst[0] == 'message' or lst[0] == 'trigger' or lst[0] == 'location' or lst[0] == 'details':
            new_key = lst[0]
            new_resource_name = 'GoogleAdsError'
            lst.append(new_resource_name)
            new_value = lst[1:]
            new_field_dict[new_key] = new_value

        elif lst[0] == 'errors[]':
            new_key = lst[0]
            new_resource_name = 'GoogleAdsFailure'
            lst.append(new_resource_name)
            new_value = lst[1:]
            new_field_dict[new_key] = new_value

        elif lst[0] == 'policy_topic_entries[]':
            new_key = lst[0]
            new_resource_name = 'PolicyFindingDetails'
            lst.append(new_resource_name)
            new_value = lst[1:]
            new_field_dict[new_key] = new_value

        elif lst[0] == 'external_policy_description' or lst[0] == 'key' or lst[0] == 'external_policy_name' or lst[0] == 'is_exemptible':
            new_key = lst[0]
            new_resource_name = 'PolicyViolationDetails'
            lst.append(new_resource_name)
            new_value = lst[1:]
            new_field_dict[new_key] = new_value

    return new_field_dict

def merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def delete_enums(lst):
    for table in lst:
        table.remove('Enums')
    return lst

flatten = lambda l: [item for sublist in l for item in sublist]

content = rq.get('https://developers.google.com/google-ads/api/reference/rpc/google.ads.googleads.v2.errors#accessinvitationerrorenum').content
soup = BeautifulSoup(content, 'lxml')

enum_name_tags = soup.find_all('code', {'class': 'apitype'})
enums = [enum.text for enum in enum_name_tags]

table_tags = soup.find_all('table', id=re.compile('ENUM_VALUES-table$'))

table_enum_name_description = [list(table.stripped_strings) for table in table_tags if list(table.strings) != '' and list(table.strings) != '\n']



resource_names = [i.text for i in soup.find_all('h2')]
remove_fields_and_enums(resource_names)

delete_enums(table_enum_name_description)

added_resource_names_dict = {}
for i in range(len(table_enum_name_description)):
    for j in range(1, len(table_enum_name_description[i]), 2):
        key = table_enum_name_description[i][j-1].replace(', ', '').replace(',', '')
        value = table_enum_name_description[i][j]
        added_resource_names_dict[key + "." + resource_names[i]] = value


############################
#Finding Fields Now
############################



field_tags = soup.find_all('section', id=re.compile('FIELDS$'))

table_field_name_type_tags = [table.find_all('td') for table in field_tags]

table_field_name_type = []
for table in table_field_name_type_tags:
    for words in table:
        table_field_name_type.append(words.code.text)
table_field_name_type.remove('error_code')

table_field_name_type_grouped = [table_field_name_type[i-2:i] for i in range(2, len(table_field_name_type), 2)]

table_field_description_tags = [table.find_all('p') for table in field_tags]

table_field_description = []
for lst in table_field_description_tags:
    for description in lst:
        table_field_description.append(list(description.stripped_strings))

table_field_descriptions_flattened = [flatten(table_field_description)[i] for i in range(1,len(flatten(table_field_description)), 2)]

for i in range(len(table_field_name_type_grouped)):
    table_field_name_type_grouped[i].append(table_field_descriptions_flattened[i])

new_field_dict = add_resource_name_to_field_new_dict(table_field_name_type_grouped)

final_dict = merge(added_resource_names_dict, new_field_dict)


with open('Google Ads Errors.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator = '\n', delimiter = ',')
    writer.writerow(['Field/Enum Name', 'ResourceName', 'Type', 'Description','\n'])
    for key, value in final_dict.items():
        #print(key, value)
        if key.split('.')[0] == key.split('.')[0].upper():
            field_enum_name = key.split('.')[0]
            resource_name = key.split('.')[1]
            print(resource_name)
            description = value
            #print(resource_name)
            #fdict = '"{}"'.format(str(fdict).replace('.', '').replace('\n', '').replace('\r', '').replace("'http", "http"))
            #f.write("%s,%s\n"%(keys, fdict))
            writer.writerow([field_enum_name, resource_name,' ', description])

        elif key != key.upper() and len(value) > 2:
            field_name = key
            resource_name = value[-1]
            description = value[1]
            type_ = value[0]
            writer.writerow([field_name, resource_name, type_, description])
