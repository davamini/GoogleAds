from bs4 import BeautifulSoup
import requests as rq
import re
import csv

def to_string(lst):
    return ' '.join(lst).replace(',', '').replace('.', '').replace('\n', '')



content = rq.get('https://developers.google.com/google-ads/api/reference/rpc/google.ads.googleads.v2.resources').content
soup = BeautifulSoup(content, 'lxml')
fields = soup.find_all("section", {"id":"index"})


for field in fields:
    names = field.find_all('a')
    index_lst = [name.text for name in names]



def get_resources(index_name):

    table_trial = soup.find("section", {"id":"google.ads.googleads.v2.resources." + str(index_name)})

    table_rows = table_trial.find_all("tr")

    field = []
    for row in table_rows:
        field.append([code.text for code in row.find_all(["p","code"])])

    Field_name_and_description = []
    for lst in field:
        if lst != []:
            new_lst = list(map(lambda s: s.strip(), lst))
            Field_name_and_description.append(new_lst)

    Field_name_and_descriptions = []
    for lst in Field_name_and_description:
        #while('' in lst):
         #   lst.remove("")

        Field_name_and_descriptions.append(list(dict.fromkeys(lst)))

    field_names = [i[0] for i in Field_name_and_descriptions]
    field_descriptions = [to_string(i[2:]) for i in Field_name_and_descriptions]
    types = [to_string(i[1:2]) for i in Field_name_and_descriptions]

    new_dict = {}
    for i in range(len(field_names)):

        new_key = field_names[i] + "." + str(index_name)

        new_dict[new_key] = types[i] + "," + field_descriptions[i] + "," + str(index_name)

    return new_dict

final_dictionary = {}
for index in index_lst:
    final_dictionary.update(get_resources(index))

with open('Google Ads Resources.csv', 'w') as f:
    f.write('FieldName, Type, FieldDescription, ResourceName\n')
    for key in final_dictionary.keys():
        if 'Union' not in key:
            keys = key.split('.')[0]
            fdict = final_dictionary[key].replace(",,","UnionField,,")
            #print("%s,%s\n"%(keys,fdict))
            f.write("%s,%s\n"%(keys,fdict))
        else:
            keys = key[11:].split('.')[0].lstrip()
            fdict = final_dictionary[key].replace(keys,"UnionField",1)
            #print("%s,%s\n"%(keys,fdict))
            f.write("%s,%s\n"%(keys,final_dictionary[key]))
