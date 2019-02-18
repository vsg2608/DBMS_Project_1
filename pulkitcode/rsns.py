import csv
path = 'zomato3.csv'
import pandas as pd
#with open(path, 'r', encoding='utf-8', errors='ignore') as infile# open('zomato_.csv', 'w', newline='') as outfile:
df = pd.read_csv('zomato3.csv', encoding = 'utf8')
cuisine = (df['Cuisines'])

listofcui = []
for row in cuisine:
    # print(row)
    if type(row) is not float: #str(row).split(',') is None:
        t = row.split(',')
        for cui in t:
            cui = cui.strip()
            if cui not in listofcui:
                listofcui.append(cui)


listofcui.sort()
id = range(1,len(listofcui)+1)
cdict = dict(zip(listofcui,id))
cdict['None'] = len(listofcui)+1
with open('dict.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in cdict.items():
       writer.writerow([key, value])
# num = 1
# listofcui = []

# rowid = 0
# cdict = {}
rid = (df['Restaurant ID'])
cuisine = (df['Cuisines'])

with open('restid_cuisineid.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # for key, value in cdict.items():
    #    writer.writerow([key, value])
    for i in range(len(rid)):
        # print(i)
        # print(type(cuisine[i]))
        if type(cuisine[i]) is not float: #str(row).split(',') is None:
            t = cuisine[i].split(',')
            for cui in t:
                cui = cui.strip()
                writer.writerow([rid[i], cdict[cui]])
        else:
            writer.writerow([rid[i], cdict['None']])
    #else:

# with open('dict.csv', 'w', newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in cdict.items():
#        writer.writerow([key, value])
