import csv
import pandas as pd

# basic csv reading
fobj = open('test_csv.csv', 'r')
reader = csv.reader(fobj)
for row in reader:
    print(row)
print('')

# read csv as a list of rows(dict)
fobj = open('test_csv.csv', 'r')
reader = csv.reader(fobj)
headers = tuple()
is_first_row = True
data_list = list()
for row in reader:
    temp_dict = dict()
    if is_first_row:
        headers = tuple(row)
        is_first_row = False
        continue
    for i in range(0, len(row)):
        temp_dict[headers[i]] = row[i]
    data_list.append(temp_dict)
print(data_list)
print('')

# using pandas
data_df = pd.read_csv('test_csv.csv', header='infer')  # column names collected from first row
print(data_df)
print('')

