#In[]
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import os
init_notebook_mode(connected=True)
cf.go_offline()

pathwayUnity = "C:\\Users\\49176\\Desktop\\Python_Scripts\\Visualization_First Trial\\Unity\\"
pathwayVicon = "C:\\Users\\49176\\Desktop\\Python_Scripts\\Visualization_First Trial\\Vicon\\"
listPathwayUni = []
listPathwayVic = []

for entry in os.listdir(pathwayUnity):
    listPathwayUni.append(entry)

for entry in os.listdir(pathwayVicon):
    listPathwayVic.append(entry)

number = 0
numExcUni = listPathwayUni[number]
numExcVic = listPathwayVic[number]
str1 = "Unity"+str(numExcUni)
str2 = "Vicon"+str(numExcVic)

def wholeDataFrame(number, numExcUni, numExcVic, str1, str2):
    df_Uni = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Visualization_First Trial\\Unity\\"+numExcUni)
    df_Vic = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Visualization_First Trial\\Vicon\\"+numExcVic)

    def collection(x,y):
        data_collection = []
        for i in x,y:
            data_collection.append(x.iloc[:,1])
            data_collection.append(y.iloc[:,1])
        return data_collection
    dataSet1 = collection(df_Uni, df_Vic)

    lengthIndex = max(len(dataSet1[0]), len(dataSet1[1]))

    if len(dataSet1[0]) != len(dataSet1[1]):
        if len(dataSet1[0])<=lengthIndex:
            for i in range(0,lengthIndex-len(dataSet1[0]),1):
                list(dataSet1[0]).append("NaN")
        if len(dataSet1[1])<=lengthIndex:
            for j in range(0,lengthIndex-len(dataSet1[1]),1):
                list(dataSet1[1]).append("NaN")
    
    dic1 = {str1:pd.Series(dataSet1[0]), str2:pd.Series(dataSet1[1])}
    return dic1
wholeDataFrame(number,numExcUni,numExcVic,str1,str2)

new_df = pd.DataFrame(wholeDataFrame(number,numExcUni,numExcVic,str1,str2))

for i in range(1,len(listPathwayUni),1):
    number += 1
    numExcUni = listPathwayUni[number]
    numExcVic = listPathwayVic[number]
    str1 = "Unity"+str(numExcUni)
    str2 = "Vicon"+str(numExcVic)
    newDataFrame = pd.DataFrame(wholeDataFrame(number,numExcUni,numExcVic,str1,str2))
    df_forLoop = pd.DataFrame(wholeDataFrame(number,numExcUni,numExcVic,str1,str2))
    new_df = pd.concat([new_df,df_forLoop])

new_df.to_csv("FinalWithoutStr.csv")
# %%
