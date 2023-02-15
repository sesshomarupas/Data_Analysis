#In[]
import numpy as np
import pandas as pd
from statistics import mean
from statistics import stdev
import csv
import os

path = "C:\\Users\\49176\\Desktop\\Python_Scripts\\Mehrere Excel Daten"
listExcel = []
for entry in os.listdir(path):
    listExcel.append(entry)
del listExcel[0]
index_List_2 = ["pre", "post", "retention"]
 
num = 0

list_Dictionaries = []

def joiningExc(num):
    data = pd.read_excel(listExcel[num])
    index_List = list(range(3))
    m1 = mean(data["pre"]); m2 = mean(data.iloc[:,1]); m3 = mean(data["retention"])
    result = pd.DataFrame({"Proband" + str(num): [m1,m2,m3]}, index= index_List)
    list_Dictionaries.append(result)
    return result
df = joiningExc(num) 

for i in range(1,len(listExcel),1):
    num+=1
    joiningExc(num)

results = pd.concat(list_Dictionaries, axis=1)
results_transpose = results.transpose()
results.to_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Mehrere Excel Daten\\results.csv")
results_transpose.to_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Mehrere Excel Daten\\results_transpose.csv")
# %%
