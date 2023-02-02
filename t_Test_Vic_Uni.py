#In[]
import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
from matplotlib import style
from statistics import mean
from statistics import stdev
import math
from scipy.stats import shapiro
from scipy.stats import kstest
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon

df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Min_Max\\LH_normal\\90Hz80Rpm\\Min_Max1.csv", sep=",", decimal=".")
sampleSize = df.shape[0]

Vicon_Minima = np.array(df.iloc[:,1][:48])
Unity_Minima = np.array(df.iloc[:,2][:48])
Vicon_Maxima = np.array(df.iloc[:,3][:48])
Unity_Maxima = np.array(df.iloc[:,4][:48])

Vicon_Min = []
Unity_Min = []
Vicon_Max = []
Unity_Max = []

def normalverteilungSha(x,y):
    y.append(list(shapiro(x)))

# Normalverteilung Minima Vicon
normalverteilungSha(df.iloc[:,1][:48], Vicon_Min)
print("statistic:{}, pvalue:{}".format(Vicon_Min[0][0],Vicon_Min[0][1]))
normalverteilungSha(df.iloc[:,2][:50], Unity_Min)
print("statistic:{}, pvalue:{}".format(Unity_Min[0][0],Unity_Min[0][1]))
normalverteilungSha(df.iloc[:,3][:49], Vicon_Max)
print("statistic:{}, pvalue:{}".format(Vicon_Max[0][0],Vicon_Max[0][1]))
normalverteilungSha(df.iloc[:,4], Unity_Max)
print("statistic:{}, pvalue:{}".format(Unity_Max[0][0],Unity_Max[0][1]))

def decisionBetween_tTests(x,y,z,h): 
    if (x[0][1] and y[0][1]) and z[0][1] and h[0][1] <= 0.05:
        def tTestRel(data1, data2):
            result = []
            stat, p = ttest_rel(data1, data2)
            result.append("stat:{}".format(stat))
            result.append("p:{}".format(p))
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            alpha = 0.05
            if p > alpha:
                print('Result: tTestRel: Same distribution (accept H0)')
            else:
                print('tTestRel: Different distribution (reject H0)')
            return result
        minima = tTestRel(Vicon_Minima, Unity_Minima)
        maxima = tTestRel(Vicon_Maxima, Unity_Maxima)
    else:
        def wilcoxonSRang(data1,data2):
            result = []
            stat, p = wilcoxon(data1, data2)
            result.append("stat:{}".format(stat))
            result.append("p:{}".format(p))
            print('Statistics=%.3f, p=%.3f' % (stat,p))
            alpha = 0.05
            if p > alpha:
                print('Result: Wilcoxon Signed Rang: Same distribution (accept H0)')
            else:
                print('Result: Wilcoxon Signed Rang: Different distribution (reject H0)')
            return result
        minima = tTestRel(Vicon_Minima, Unity_Minima)
        maxima = tTestRel(Vicon_Maxima, Unity_Maxima)
        
decisionBetween_tTests(Vicon_Min, Vicon_Max, Unity_Min, Unity_Max)



# %%
