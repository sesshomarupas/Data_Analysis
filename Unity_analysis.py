#In[] Importieren der Bibliotheken 
import numpy as np
import pandas as pd
import math
from math import acos
from math import sqrt
import statistics
import matplotlib.pyplot as plt
from matplotlib import style
excelSheet = 1
mode = 1
lighthouse_Pos = 1
hertz = 90
rpm = 80

def mult_Excel(excelSheet, mode, lighthouse_Pos, hertz, rpm):  
#In[] Neuen Unity_Datensatz einlesen und umwandeln
    df_Unity_Feet = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"n\\Fuss"+" "+ str(hertz)+ " " + str(rpm)+ " n " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
    df_Unity_Hip = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"n\\Huefte"+" "+ str(hertz)+ " " + str(rpm)+ " n " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
    df_Unity_Knee = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"n\\Knie"+" "+ str(hertz)+ " " + str(rpm)+ " n " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
    fig_Name_VR = 1

    def wholeCalculationVR(df_Unity_Feet,df_Unity_Hip,df_Unity_Knee, fig_Name_VR, mode, lighthouse_Pos):
        
        time_Unity = df_Unity_Feet.iloc[:,0]

        kneeTracker_VR = (df_Unity_Knee.iloc[:,3], df_Unity_Knee.iloc[:,2], df_Unity_Knee.iloc[:,1]) # x, y, z
        feetTracker_VR = (df_Unity_Feet.iloc[:,3], df_Unity_Feet.iloc[:,2], df_Unity_Feet.iloc[:,1])
        hipTracker_VR = (df_Unity_Hip.iloc[:,3], df_Unity_Hip.iloc[:,2], df_Unity_Hip.iloc[:,1])

        xKT_VR = kneeTracker_VR[0]
        xFT_VR = feetTracker_VR[0]
        xHT_VR = hipTracker_VR[0]
        yKT_VR = kneeTracker_VR[1]
        yFT_VR = feetTracker_VR[1]
        yHT_VR = hipTracker_VR[1]
        zKT_VR = kneeTracker_VR[2]
        zFT_VR = feetTracker_VR[2]
        zHT_VR = hipTracker_VR[2]

        def funcVec_a():
            vector1 = list()
            for i in range(df_Unity_Feet.shape[0]):
                vecKneeToFeet = sqrt((xKT_VR[i]-xFT_VR[i])**2+(yKT_VR[i]-yFT_VR[i])**2+(zKT_VR[i]-zFT_VR[i])**2)
                vector1.append(vecKneeToFeet)
            return vector1
        vector_a = pd.DataFrame(funcVec_a())
        vector_a_Arr_VR = vector_a.to_numpy()

        def funcVec_b():
            vector2 = list()
            for i in range(df_Unity_Feet.shape[0]):
                vecKneeToHip = sqrt((xKT_VR[i]-xHT_VR[i])**2+(yKT_VR[i]-yHT_VR[i])**2+(zKT_VR[i]-zHT_VR[i])**2)
                vector2.append(vecKneeToHip)
            return vector2
        vector_b = pd.DataFrame(funcVec_b())
        vector_b_Arr_VR = vector_b.to_numpy()

        def funcVec_c():
            vector3 = list()
            for i in range(df_Unity_Feet.shape[0]):
                vecHipToFeet = sqrt((xFT_VR[i]-xHT_VR[i])**2+(yFT_VR[i]-yHT_VR[i])**2+(zFT_VR[i]-zHT_VR[i])**2)
                vector3.append(vecHipToFeet)
            return vector3
        vector_c = pd.DataFrame(funcVec_c())
        vector_c_Arr_VR = vector_c.to_numpy()

        directVectors_3D_VR = (vector_a_Arr_VR, vector_b_Arr_VR, vector_c_Arr_VR)

        a_VR = directVectors_3D_VR[0]
        b_VR = directVectors_3D_VR[1]
        c_VR = directVectors_3D_VR[2]
        anglesVR = list()
        for i in range (df_Unity_Feet.shape[0]):
            angle_trials = (acos((a_VR[i]**2 + b_VR[i]**2 - c_VR[i]**2)/(2*a_VR[i]*b_VR[i])))
            anglesVR.append(angle_trials)

        angleList_VR = list()
        for i in anglesVR:
            i = math.degrees((i))
            angleList_VR.append(i)

        # Abspeichern der Figures und Winkelberechnungen
        LH_P = None
        if lighthouse_Pos == 1:
            LH_P = "LH_normal"
        elif lighthouse_Pos == 2:
            LH_P = "LH_special"

        colors = ("black","green","blue","red")
        style.use('ggplot')
        fig, ax = plt.subplots(figsize=(8,6))
        plt.plot(time_Unity, angleList_VR, linewidth=2, alpha=0.75, color=colors[fig_Name_VR])
        ax.grid(True, color="k")
        plt.title('Angle Time Measurements Unity')
        plt.ylabel('Angle in °')
        plt.xlabel('Time in Seconds')
        plt.ylim(50,150)
        plt.savefig('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\'+LH_P+'\\Figures\\'+str(hertz)+'Hz'+str(rpm)+'Rpm\\Figures' + str(fig_Name_VR) + "_" + str(mode) +'.png', dpi=300, bbox_inches='tight')

        col1 = "Time"
        col2= "Angles"
        angleList_VR = pd.DataFrame(angleList_VR)
        dataAngles = pd.DataFrame({col1:time_Unity,col2:angleList_VR[0]})
        dataAngles.to_csv('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\'+LH_P+'\\AngleData\\'+str(hertz)+'Hz'+str(rpm)+'Rpm\\AngleData' + str(fig_Name_VR) + "_" + str(mode) + '.csv')

    wholeCalculationVR(df_Unity_Feet,df_Unity_Hip,df_Unity_Knee, fig_Name_VR, mode, lighthouse_Pos)

    def repWC_special():
        df_Unity_Feet = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"s\\Fuss"+" "+ str(hertz)+ " " + str(rpm)+ " s " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
        df_Unity_Hip = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"s\\Huefte"+" "+ str(hertz)+ " " + str(rpm)+ " s " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
        df_Unity_Knee = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"s\\Knie"+" "+ str(hertz)+ " " + str(rpm)+ " s " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
        mode = 2
        lighthouse_Pos = 2
        wholeCalculationVR(df_Unity_Feet,df_Unity_Hip,df_Unity_Knee, fig_Name_VR, mode, lighthouse_Pos)
    repWC_special()

    for i in range(0,2,1):
        excelSheet += 1
        fig_Name_VR += 1
        def repWC_normal():
            df_Unity_Feet = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"n\\Fuss"+" "+ str(hertz)+ " " + str(rpm)+ " n " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
            df_Unity_Hip = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"n\\Huefte"+" "+ str(hertz)+ " " + str(rpm)+ " n " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
            df_Unity_Knee = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"n\\Knie"+" "+ str(hertz)+ " " + str(rpm)+ " n " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
            wholeCalculationVR(df_Unity_Feet,df_Unity_Hip,df_Unity_Knee, fig_Name_VR, mode, lighthouse_Pos)
        repWC_normal()

        def repWC_special():
            df_Unity_Feet = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"s\\Fuss"+" "+ str(hertz)+ " " + str(rpm)+ " s " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
            df_Unity_Hip = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"s\\Huefte"+" "+ str(hertz)+ " " + str(rpm)+ " s " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
            df_Unity_Knee = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Unity\\"+str(hertz)+" "+str(rpm)+" "+"s\\Knie"+" "+ str(hertz)+ " " + str(rpm)+ " s " +str(excelSheet)+".csv", sep=";", decimal=",", skiprows=1, encoding='latin1')
            mode = 2
            lighthouse_Pos = 2
            wholeCalculationVR(df_Unity_Feet,df_Unity_Hip,df_Unity_Knee, fig_Name_VR, mode, lighthouse_Pos)
        repWC_special()

mult_Excel(excelSheet, mode, lighthouse_Pos, hertz, rpm)
# %%
