import json
import datetime
import pandas as pd
import os
import glob
import csv


def _generate_file_name(report_name:str):
    e = datetime.datetime.now()
    date="%s-%s-%s" % (e.day, e.month, e.year)
    time="%s.%s.%s" % (e.hour, e.minute, e.second)
    file_name=f"{report_name}D{date}T{time}.csv"
    return file_name

def _write_to_json(data:list,file_name):
    with open(file_name, 'w') as file_object:  #open the file in write mode
        json.dump(data, file_object)   # json.dump() function to stores the set of numbers in numbers.json file

def _write_to_csv(data:list,file_name,columns=[]):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_name, index=False)

def find_csv(name):
    path = os.getcwd()
    extension = 'csv'
    os.chdir(path)
    result = glob.glob((name+'*.{}').format(extension))
    return result[0]

def read_csv(name)->list:
    file=open(find_csv(name))
    csvreader=csv.reader(file)
    header=next(csvreader)
    rows=[]
    for row in csvreader:
        rows.append(row)
    return rows