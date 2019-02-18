# import csv
#
# path =  'zomato.csv'
#
# with open(path, 'r', encoding='utf-8', errors='ignore') as infile, open('zomato2.csv', 'w') as outfile:
#      inputs = csv.reader(infile)
#      output = csv.writer(outfile)
#      count = 0;
#      for index, row in enumerate(inputs):
#          # Create file with no header
#          try:
#              output.writerow(row)
#          except UnicodeEncodeError:
#              print(index)
#      print("count+",count)
#
import csv

path =  'Country_Code.csv'

with open(path, 'r', encoding='utf-8', errors='ignore') as infile, open('zomato3.csv', 'w', newline='') as outfile:
     inputs = csv.reader(infile)
     output = csv.writer(outfile)
     count = 0
     for index, row in enumerate(inputs):
         # Create file with no header
         try:
             output.writerow(row)
             #print(row)
         except UnicodeEncodeError:
             print(index)
     print("count+",count)



