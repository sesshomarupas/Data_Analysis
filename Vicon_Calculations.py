#In[]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import statistics
from statistics import mean
from statistics import stdev
import seaborn as sn
import math
from math import acos
from math import sqrt
import os
from scipy.signal import find_peaks

# Standard values
hertzVicon = 90.0225

pathWayVicon = "C:\\Users\\49176\\Desktop\\Python_Scripts\\Tracker_Validierung\\Rohdaten\\Vicon\\90 Hz\\"

listPathwayVicon = []
for entry in os.listdir(pathWayVicon):
    listPathwayVicon.append(entry)

number = 0

def fullCalc(number):
    dataVicon = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Tracker_Validierung\\Rohdaten\\Vicon\\90 Hz\\"+listPathwayVicon[number], delimiter=";", skiprows=4)

    # Conversion frames in seconds
    timeViconFrames = dataVicon.iloc[:,0]
    timeViconSeconds = []
    for i in timeViconFrames:
        i = i/hertzVicon
        timeViconSeconds.append(i)

    # Data for each tracker
    kneeTracker = (dataVicon.iloc[:,5], dataVicon.iloc[:,6], dataVicon.iloc[:,7]) # x,y,z
    feetTracker = (dataVicon.iloc[:,8], dataVicon.iloc[:,9], dataVicon.iloc[:,10])
    hipTracker = (dataVicon.iloc[:,2], dataVicon.iloc[:,3], dataVicon.iloc[:,4])

    # Defining new data frame for cutting 
    df = pd.DataFrame({"Time": timeViconSeconds, "Hip_X": hipTracker[0], "Hip_Y": hipTracker[1], "Hip_Z": hipTracker[2],
    "Knee_X":kneeTracker[0], "Knee_Y" : kneeTracker[1], "Knee_Z": kneeTracker[2],
    "Feet_X": feetTracker[0], "Feet_Y": feetTracker[1], "Feet_Z": feetTracker[2],})

    # Detection of the startpoint by considering the y-axis (knee rash)
    minKneePos_Y = np.where(df["Knee_Y"]==min(df["Knee_Y"]))
    timeKneePos_Min = df["Time"][minKneePos_Y[0]]
    endTime = []
    df = df[minKneePos_Y[0][0]:]
    for i in df["Time"]:
        if i <= 30+ int(timeKneePos_Min):
            endTime.append(i)
    maxTime = endTime[-1:]

    # Detetcting the end of recording time by detecting the index of the last data point less than 30 Seconds
    timeMax_Index = np.where(df["Time"]==maxTime[0])
    df = df[:timeMax_Index[0][0]]

    def visualizationFirstCut(timeKneePos_Min):
        style.use('ggplot')
        fig = plt.figure()
        meanKneeTracker = mean(df["Knee_Y"])
        plt.plot(df.iloc[:,0], df.iloc[:,5], color="black")
        plt.axhline(y=meanKneeTracker, xmin=0, xmax=1)
        plt.plot(timeKneePos_Min, min(df["Knee_Y"]),marker="v",markersize=8,color="red")
        plt.title('rash of the knee on the y-axis')
        plt.ylabel('Distance in mm')
        plt.xlabel('Time in seconds')
        plt.tight_layout()
        plt.savefig("C:\\Users\\49176\\Desktop\\Python_Scripts\\Tracker_Validierung\\Figures\\Knee_Rash\\Vicon\\"+listPathwayVicon[number][:-4]+"_Rash of the knee.jpg", dpi=300)

    visualizationFirstCut(timeKneePos_Min)

    #Lenght calculation
    df.reset_index(inplace=True)
    del df["index"]

    kneeTracker = (df.iloc[:,4], df.iloc[:,5], df.iloc[:,6]) # x,y,z
    feetTracker = (df.iloc[:,7], df.iloc[:,8], df.iloc[:,9])
    hipTracker = (df.iloc[:,1], df.iloc[:,2], df.iloc[:,3])

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

    angles = pd.Series(angleCalc(vectorKn_Ft, vectorKn_Hip, vectorHip_Ft))
    angleList = list()
    for i in angles:
        i = math.degrees((i))
        angleList.append(i)

    angles_and_lengths = pd.DataFrame({"Time": df["Time"], "Angles": angleList, "Length_Kn_Ft": vectorKn_Ft,
     "Length_Kn_Hip": vectorKn_Hip, "Length_Hip_Ft": vectorHip_Ft})
    angles_and_lengths.to_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Tracker_Validierung\\Längen\\Vicon\\"+listPathwayVicon[number][:-4]+"_Angles and Lengths.csv")

    # Minima and Maxima
    angles_arr = np.array(angleList)
    maxima = list(find_peaks(angles_arr, height=0)[1]["peak_heights"])
    minima_first = list(find_peaks(-angles_arr, height=-100)[1]["peak_heights"])
    minima = []
    for i in minima_first:
        i = abs(i)
        minima.append(i)
    amount_of_maxima = len(minima)
    amount_of_minima = len(maxima)

    style.use('ggplot')
    fig1 = plt.figure()
    plt.plot(maxima, marker="o", color="green")
    plt.plot(minima, marker="v", color="black")
    plt.title('rash of the knee on the y-axis')
    plt.ylabel('Distance in mm')
    plt.xlabel('Amount of extrema')
    plt.tight_layout()
    plt.savefig("C:\\Users\\49176\\Desktop\\Python_Scripts\\Tracker_Validierung\\Figures\\Extrema\\Vicon\\"+listPathwayVicon[number][:-4]+"_Min_and_Max.jpg",dpi=300)

    dic_Min_and_Max = pd.DataFrame({"Vicon_Minima":pd.Series(minima), "Vicon_Maxima":pd.Series(maxima)})
    dic_Min_and_Max.to_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Tracker_Validierung\\Extrema\\Vicon\\"+listPathwayVicon[number][:-4]+"_Min and Max.csv")

fullCalc(number)

for i in range(1, len(listPathwayVicon),1):
    number+=1
    fullCalc(number)
# %%
