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
import time 
from time import process_time
numExcel = 0

def multipleExcel(numExcel):
    start_time = process_time()
    borderBAP = 1.96
    df = pd.read_csv("Messsysteme" + str(numExcel) + ".csv", sep=";")
    numFig = 1

    def blandAltmanDiagramm(df, numFig): 
        messSystem1 = df.iloc[:,0]
        messSystem2 = df.iloc[:,1]
        sampleSize = messSystem1.shape[0]

        differenz = list()
        mittelwert = list()

        for i in range (df.shape[0]):
            substraction = (messSystem1[i]-messSystem2[i])
            meanCal = ((messSystem1[i]+messSystem2[i])/2)
            differenz.append(substraction)
            mittelwert.append(meanCal)

        midDif = mean(differenz)
        stdDif = stdev(differenz)
        borderUp = midDif+stdDif*borderBAP
        borderDown = midDif-stdDif*borderBAP

        print("Der Mittelwert der Differenz beträgt: ", [midDif],\
            "die Standardabweichung beträgt: ", [stdDif],\
            "die obere Grenze beträgt: ", [borderUp],\
                "die untere Grenze beträgt: ", [borderDown])
            
        if sampleSize <= 20:
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
        plt.ylim(-1,3.5)
        plt.savefig('Bland-Altman_Diagramm' + str(numFig) + '.png', dpi=300, bbox_inches='tight')
        #plt.show()
            
    blandAltmanDiagramm(df, numFig)

    for i in range(0,4,1):
        numExcel+=1
        numFig += 1
        def repetitionBAP():
            df = pd.read_csv("Messsysteme" + str(numExcel) + ".csv", sep=";")
            blandAltmanDiagramm(df, numFig)
        repetitionBAP()
      
    endtime = process_time()
    print(endtime-start_time)

multipleExcel(numExcel)