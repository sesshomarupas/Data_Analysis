#In[]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from statistics import mean
from statistics import stdev
import math
import csv
from scipy.stats import shapiro
from scipy.stats import kstest

condition = 1 # Lighthouse position, 1 = LH normal, 2 = LH special 
hertz = 90
rpm = 80

def calc_BlandAltMan(condition,hertz,rpm):
    pathway = None
    if condition == 1:
        pathway = "LH_normal"
    elif condition ==2:
        pathway = "LH_special"

    df_Vicon = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Vicon\\"+pathway+"\\"+str(hertz)+"Hz"+str(rpm)+"Rpm\\AngleData1_"+str(condition)+".csv"
    ,sep=",",decimal=".",skiprows=1)

    df_Unity = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Unity\\"+pathway+"\\"+str(hertz)+"Hz"+str(rpm)+"Rpm\\AngleData1_"+str(condition)+".csv"
    ,sep=",",decimal=".",skiprows=1)

    DataVicon = df_Vicon.iloc[:,2]
    DataUnity = df_Unity.iloc[:,2]
    Sample_Size = DataVicon.shape[0]
    borderBAP = 1.96

    differenz = []
    mittelwert = []

    for i in range (df_Vicon.shape[0]):
        substraction = abs(DataVicon[i]-DataUnity[i])
        meanCal = ((DataVicon[i]+DataUnity[i])/2)
        differenz.append(substraction)
        mittelwert.append(meanCal)

    midDif = mean(differenz)
    stdDif = stdev(differenz)
    borderUp = midDif+stdDif*borderBAP
    borderDown = midDif-stdDif*borderBAP

    print("Der Mittelwert der Differenz beträgt {}: "\
                "die Standardabweichung beträgt: {}"\
                "die obere Grenze beträgt: {}"\
                    "die untere Grenze beträgt: {}".format(midDif, stdDif, borderUp,borderDown))

    if Sample_Size <= 20:
        def normalverteilung():
            resultShapiroWilk = []
            shapiroTest = shapiro(differenz)
            resultShapiroWilk.append(shapiroTest)
            return shapiroTest, resultShapiroWilk
        print(normalverteilung())

    else:
        def normalverteilungKS():
            resultKTest = []
            ksTest = kstest(differenz, 'norm')
            resultKTest.append(ksTest)
            return ksTest, resultKTest
        print(normalverteilungKS())

    style.use('ggplot')
    fig, ax = plt.subplots(figsize=(8,6))
    plt.scatter(mittelwert, differenz, linewidth=2, alpha=0.75, color='black', s=45) #label = "name"
    plt.axhline(y=midDif, xmin=0, xmax=1)
    plt.axhline(y=borderUp, xmin=0, xmax=1, color="blue")
    plt.axhline(y=borderDown, xmin=0, xmax=1, color="blue")
    ax.legend()
    ax.grid(True, color="k")
    plt.title('Scatter chart')
    plt.ylabel('Differences between the measurement systems')
    plt.xlabel('Mean (Differences)')
    plt.ylim(-10,65)
    plt.savefig("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Figures\\"+pathway+"\\"+str(hertz)+"Hz"+str(rpm)+"Rpm\\"+str(hertz)+"Hz"+str(rpm)+"Rpm.png", dpi=300, bbox_inches='tight')

calc_BlandAltMan(condition,hertz,rpm)
# %%
