#In[]
import numpy as np
import pandas as pd
import math
from math import acos
from math import sqrt
import statistics
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

hertzVicon = 90.0225 
rpm = 80

df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Minima_Maxima_Angles\\90Hz_80rpm_01.csv", sep=";", skiprows=4, encoding='latin1')

time_Vicon = df.iloc[:,0]
timeViconModified = []
for i in time_Vicon: 
       newTime = i/hertzVicon
       timeViconModified.append(newTime)
time_as_array = np.array(timeViconModified)
time_as_series = pd.Series(time_as_array)
time_as_list = list(time_as_array)
timeMax = timeViconModified[-1:][0]

kneeTracker = (df.iloc[:,5], df.iloc[:,6], df.iloc[:,7]) # x,y,z
feetTracker = (df.iloc[:,8], df.iloc[:,9], df.iloc[:,10])
hipTracker = (df.iloc[:,2], df.iloc[:,3], df.iloc[:,4])

def funcLengthVec(x,y,z,x2,y2,z2):
    vector = list()
    for i in range(df.shape[0]):
        vec_Calc = sqrt((x2[i]-x[i])**2+(y2[i]-y[i])**2+(z2[i]-z[i])**2)
        vector.append(vec_Calc)
    return vector

vectorKn_Ft = pd.Series(funcLengthVec(feetTracker[0], feetTracker[1], feetTracker[2], kneeTracker[0], kneeTracker[1], kneeTracker[2])) # Vector a

vectorKn_Hip = pd.Series(funcLengthVec(kneeTracker[0], kneeTracker[1], kneeTracker[2], hipTracker[0],hipTracker[1],hipTracker[2])) # Vector b

vectorHip_Ft = pd.Series(funcLengthVec(feetTracker[0], feetTracker[1], feetTracker[2],hipTracker[0],hipTracker[1],hipTracker[2])) # Vector c

def angleCalc(a,b,c):
    angles = list()
    for i in range(df.shape[0]):
        angle_trials = (acos((a[i]**2 + b[i]**2 - c[i]**2)/(2*a[i]*b[i])))
        angles.append(angle_trials)
    return angles

angles_Series = pd.Series(angleCalc(vectorKn_Ft, vectorKn_Hip, vectorHip_Ft))

angleList = list()
for i in angles_Series:
    i = math.degrees((i))
    angleList.append(i)

df_new = {"Time_Unmodified": time_Vicon, "Time": time_as_series, "Angles": angleList, "Length_Kn_Ft": vectorKn_Ft,
 "Length_Kn_Hip": vectorKn_Hip, "Length_Hip_Ft": vectorHip_Ft}

df_Dataframe = pd.DataFrame(df_new)
df_Dataframe_dropped = df_Dataframe[0:100]
df_Dataframe.to_csv("Dataset_Lengths.csv")

# Preparation for the min and max values for each time intervall
angle_var = df_Dataframe["Angles"]
timeIntervall = 60/rpm

def calc_min_max(df_Dataframe, time_as_series, angleList, timeIntervall):
    angles_per_intervall_Max = [] 
    angles_per_intervall_Min = [] 
    startTime = df_Dataframe.iloc[0,1] 
    endTime = startTime + timeIntervall
    def innerFunc(startTime, endTime):  
        list_perIntervall = []
        for i in range(0,df_Dataframe.shape[0],1):
            if df_Dataframe.iloc[i,1] <= endTime:
                list_perIntervall.append(df_Dataframe.iloc[i,2])
            else:
                startTime = endTime
                endTime = startTime + timeIntervall 
                continue   
        angles_per_intervall_Max.append(max(list_perIntervall))
        angles_per_intervall_Min.append(min(list_perIntervall)) 
        return angles_per_intervall_Min, angles_per_intervall_Max
    result = {"Minima": innerFunc(startTime, endTime)[0], "Maxima":innerFunc(startTime, endTime)[1]}
    return result

min_max_df = pd.Series(calc_min_max(df_Dataframe, time_as_series, angle_var, timeIntervall))
data_Min_Max = pd.DataFrame(min_max_df)

# Min und Max bestimmen
from scipy.signal import argrelextrema
angles_Max = np.array(angleList)[argrelextrema(np.array(angleList), np.greater)] # Rohwerte
angles_Min = np.array(angleList)[argrelextrema(np.array(angleList), np.less)]
index_maxima = argrelextrema(np.array(angleList), np.greater) # Index
index_minima = argrelextrema(np.array(angleList), np.less)
time_max = df_Dataframe.iloc[index_maxima[0],1] # nur bei dem Index von index_max/min die Zeit ausgeben
time_min = df_Dataframe.iloc[index_minima[0],1]
dataSet_min_max = {"Minima":time_min, "Maxima":time_max}
dataSet_M_M_Df = pd.DataFrame(dataSet_min_max)
dataSet_M_M_Df.to_csv("Dataset Minima and Maxima.csv") 

style.use('ggplot')
plt.subplot(2,2,1)
plt.plot(time_as_series, angleList, linewidth=2, alpha=0.75, color="black")
plt.title('Angles Vicon System')
plt.ylabel('Angle in °')
plt.xlabel('Time in seconds')
plt.ylim(50,150)
plt.tight_layout()

plt.subplot(2,2,2)
plt.plot(time_as_series, kneeTracker[1], linewidth=2, alpha=0.75, color="b")
plt.title('Y Coordinates KneeTracker')
plt.ylabel('mm')
plt.xlabel('Time in seconds')
plt.tight_layout()

plt.subplot(2,2,3)
plt.plot(time_as_series, feetTracker[1], linewidth=2, alpha=0.75, color="g")
plt.title('Y Coordinates FeetTracker')
plt.ylabel('mm')
plt.xlabel('Time in seconds')
plt.tight_layout()

plt.subplot(2,2,4)
plt.plot(time_as_series, hipTracker[1], linewidth=2, alpha=0.75, color="r")
plt.title('Y Coordinates HipTracker')
plt.ylabel('mm')
plt.xlabel('Time in seconds')
plt.tight_layout()
plt.savefig("Angles_Coordinates.png")

af = plt.figure()
axes = af.add_axes([0.1,0.1,0.8,0.8])
axes.plot(time_as_series, kneeTracker[1],'b')
axes.set_xlabel('Time in seconds')
axes.set_ylabel('mm')
axes.set_title('Ausholbewegung')
plt.savefig("Y Auslenkung.png")

new_fig = plt.figure()
axes_new = new_fig.add_axes([0.1,0.1,0.8,0.8])
axes_new.plot(time_as_series, angleList,'g')
axes_new.set_xlabel('Time in seconds')
axes_new.set_ylabel('Angles in degree')
axes_new.set_title('Angles')

#In[] min and max plot
min_max_fig = plt.figure()
axes = min_max_fig.add_axes([0.5,0.1,0.8,0.8])
axes.plot(time_max,angles_Max,'red')
axes.plot(time_min,angles_Min,'blue')
axes.set_title('minima and maxima of the angles')
axes.set_xlabel("Time")
axes.set_ylabel("Angles")
plt.ylim(60,140)
#sns.displot(angles_Max)
#sns.displot(angles_Min)
#sns.stripplot(x=angles_Max)
#sns.stripplot(x=angles_Min)
# %%
