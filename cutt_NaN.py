#In[] 
import numpy as np
import pandas as pd

data = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Datensatz_angleichen_NaNs\\datensatz.csv", delimiter=";")
index_NaN = []

with open("datensatz.csv", "r") as file:
    for line in file:
        index_NaN += [line.strip()]

corr_List = []
for i in index_NaN:
    if ("NaN" not in i):
            corr_List.append(i.split(";"))

result = pd.DataFrame(corr_List)
index_File = []
number = 1
for i in range(0, (result.shape[0]), 1):
    index_File.append("Proband " + str(number))
    number+=1
index_File.insert(0, "Teilnehmer"); index_File = index_File[:-1]
result = pd.DataFrame(corr_List, index=index_File, columns=["Time_1", "Time_2", "Time_3"])

result.iloc[1:,:].to_csv("result.csv")
#In[] Einlesen des Datensatzes 
import numpy as np
import pandas as pd

data2 = pd.read_csv("d2.csv", delimiter=";")

# In welchen Spalten befinden sich NaN Values:
columns_NaN = data2.columns[data2.isnull().any()].to_list()
nan_cols = [i for i in data2.columns if data2[i].isnull().any()]

# Die vollständigen Spalten anzeigen, in der sich NaN befinden
rowsNaN = data2.loc[:, data2.isnull().any()]

# Boolean Ausgabe der Spalten mit NaNs
dataFrameTrueFalse = data2.isnull().any()

# Reihenidentifikation, in denen NaNs sind über den Index
nan_rows = data2[data2.isnull().T.any()].index
num = 0
def changingDF(num):
    for i in range(0, len(nan_rows), 1): 
        data2.drop(nan_rows[num], axis=0, inplace=True)
        num+=1
changingDF(num)
data2.reset_index()
# %%
