#In[]
import pandas as pd
import numpy as np
from statistics import mean
from statistics import median
from statistics import stdev
import os
from statsmodels import robust

pathWay = "C:\\Users\\49176\\Desktop\\Python_Scripts\\Außreißer_Indentifizierung\\Auswertung Basti\\Differences"

listPathways = []
for entry in os.listdir(pathWay):
    listPathways.append(entry)

number = 0
numExc = listPathways[number]

def runAllData(number,numExc):
    df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Außreißer_Indentifizierung\\Auswertung Basti\\Differences\\"+numExc)

    amount_of_Outliers = []
    deltaValue = list(df.iloc[:,1])
    deltaPercentage = list(df.iloc[:,2])
    deltaTime = list(df.iloc[:,3])

    def func_outliers(x):

        medianDiffx = median(x)
        mad = robust.mad(x)
        borderUpx = medianDiffx + 3*mad
        borderDownx = medianDiffx - 3*mad

        deltaValue_withOut = []

        for i in x:
            if i > borderUpx or i < borderDownx:
                deltaValue_withOut.append("NaN")
            else:
                deltaValue_withOut.append(i)
   
        df_without_outliers = {"deltaValue_withOut": deltaValue_withOut}
        dataFrame_without_Outliers = pd.DataFrame(df_without_outliers)
        dataFrame_without_Outliers.to_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Außreißer_Indentifizierung\\Differences_withOut\\"+numExc)
    func_outliers(deltaValue)
    
runAllData(number, numExc)

for i in range(1,len(listPathways),1):
    number = number + 1
    numExc  = listPathways[number]
    runAllData(number, numExc)
# %%
