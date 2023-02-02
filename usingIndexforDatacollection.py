#In[]
import pandas as pd
import numpy as np
from statistics import mean

df = pd.read_excel("Data.xlsx")

data = df.iloc[:,0]
codierung = df.iloc[:,1]
dataIndex = df.index
dataCodierung_1 = np.where(codierung==1)[0] # right-handed Data encoded with 1
dataCodierung_2 = np.where(codierung==2)[0] # left-handed Data encoded with 2

def firstFunc(data, codierung): # not necessary, just saving the values from one column indicated by values from another
    data_1 = []
    data_2 = []
    for i in range(df.shape[0]):
        if codierung[i] == 1:
            data_1.append(data[i])
        else:
            data_2.append(data[i])     
    return data_1, data_2

results = firstFunc(data,codierung)

data_withCode_1 = data[dataCodierung_1] # creating a new list for right-handed Data by using the index
data_withCode_2 = data[dataCodierung_2]

dicDataFrame = {"data": pd.Series(data), "Codierung": pd.Series(codierung), 
"Index_von_1":pd.Series(dataCodierung_1), "Index_von_2":pd.Series(dataCodierung_2),
"Data_Codierung_1": pd.Series(data_withCode_1), "Data_Codierung_2":pd.Series(data_withCode_2)}

pd.DataFrame(dicDataFrame).to_csv("DataFrame.csv")

right_handed_data = pd.DataFrame(dicDataFrame).iloc[:,4]
left_handed_data = pd.DataFrame(dicDataFrame).iloc[:,5]

chunk_size = 10 
# split list into 10 equal sized parts
splitRightHandData = list([right_handed_data[i:i+chunk_size] for i in range(0,len(right_handed_data),chunk_size)])
splitLeftHandData = list([left_handed_data[i:i+chunk_size] for i in range(chunk_size,len(left_handed_data),chunk_size)])

# Saving every second element in new list
def newListCreation(x,y):
    RHL = []
    LHL = []
    for i in x[::2]:
        RHL.append(i)
    for i in y[::2]:
        LHL.append(i)
    return RHL, LHL

RH_Intervall = newListCreation(splitRightHandData,splitLeftHandData)[0]
LH_Intervall = newListCreation(splitRightHandData, splitLeftHandData)[1]

# saving the last value of each list as float 
LastValueRH = []
LastValueLH = []

for  i in RH_Intervall:
    i = float(i[-1:])
    LastValueRH.append(i)
for i in LH_Intervall:
    i = float(i[-1:])
    LastValueLH.append(i)

dicResults = {"RightHand_Reaktion": pd.Series(LastValueRH), 
"LeftHand_Reaktion": pd.Series(LastValueLH)}

pd.DataFrame(dicResults).to_csv("ResultsReactionTime.csv")
# %%
