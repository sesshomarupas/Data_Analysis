#In[]
import pandas as pd
import numpy as np
from statistics import mean
from statistics import median
from statistics import stdev
import os
from statsmodels import robust

pathWayUnity = "C:\\Users\\49176\\Desktop\\Python_Scripts\\Außreißer_Indentifizierung\\Auswertung Basti\\Unity"

listPathwaysUnity = []
for entry in os.listdir(pathWayUnity):
    listPathwaysUnity.append(entry)

number = 0
numExc = listPathwaysUnity[number]

def runAllData(number,numExc):
    df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Außreißer_Indentifizierung\\Auswertung Basti\\Unity\\"+numExc)

    amount_of_Outliers = []
    angles = list(df.iloc[:,2])

    def func_outliers(x):
        medianDiffx = median(x)
        mad = robust.mad(x)
        borderUpx = medianDiffx + 3*mad
        borderDownx = medianDiffx - 3*mad

        angles_withOut = []

        for i in x:
            if i > borderUpx or i < borderDownx:
                angles_withOut.append("NaN")
            else:
                angles_withOut.append(i)

        df_without_outliers = {"angle_withOut": angles_withOut}
        dataFrame_without_Outliers = pd.DataFrame(df_without_outliers)
        dataFrame_without_Outliers.to_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Außreißer_Indentifizierung\\angles_withOut\\Unity\\"+numExc)    
    func_outliers(angles)
    
runAllData(number, numExc)

for i in range(1,len(listPathwaysUnity),1):
    number = number + 1
    numExc  = listPathwaysUnity[number]
    runAllData(number, numExc)
# %%
