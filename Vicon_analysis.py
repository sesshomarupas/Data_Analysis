#In[] Importieren der Bibliotheken 
import numpy as np
import pandas as pd
import math
from math import acos
from math import sqrt
import statistics
import matplotlib.pyplot as plt
from matplotlib import style

excelSheet = 1 # Nummer der Excel Datei einlesen 
mode = 1 # _s an die Datei anhängen
lighthouse_Pos = 1 # In Lighthouse-Ordner abspeichern
hertz = 200
rpm = 120

#In[] Einlesen des Datensatzes von Vicon

def mult_Excel(excelSheet, mode, lighthouse_Pos, hertz, rpm):    
    df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\Vicon\\"+str(hertz)+"Hz_"+str(rpm)+"rpm_0" + str(excelSheet) + ".csv", sep=";", skiprows=4, encoding='latin1')
    fig_Name = 1

    # Globale Funktion: Längenberechnung der Richtungsvektoren a,b,c
    def wholeCalculation(df, fig_Name, mode, lighthouse_Pos):
        kneeTracker = (df.iloc[:,5], df.iloc[:,6], df.iloc[:,7])
        feetTracker = (df.iloc[:,8], df.iloc[:,9], df.iloc[:,10])
        hipTracker = (df.iloc[:,2], df.iloc[:,3], df.iloc[:,4])

        def funcDirectionVectors():
            xKT = kneeTracker[0]
            xFT = feetTracker[0]
            xHT = hipTracker[0]
            yKT = kneeTracker[1]
            yFT = feetTracker[1]
            yHT = hipTracker[1]
            zKT = kneeTracker[2]
            zFT = feetTracker[2]
            zHT = hipTracker[2]

            # Berechnung der Länge jedes einzelnen Vektors
            def funcVec_a():
                vector1 = list()
                for i in range(df.shape[0]):
                    vecKneeToFeet = sqrt((xKT[i]-xFT[i])**2+(yKT[i]-yFT[i])**2+(zKT[i]-zFT[i])**2)
                    vector1.append(vecKneeToFeet)
                return vector1
            vector_a = pd.DataFrame(funcVec_a())
            vector_a_Arr = vector_a.to_numpy()

            def funcVec_b():
                vector2 = list()
                for i in range(df.shape[0]):
                    vecKneeToHip = sqrt((xKT[i]-xHT[i])**2+(yKT[i]-yHT[i])**2+(zKT[i]-zHT[i])**2)
                    vector2.append(vecKneeToHip)
                return vector2
            vector_b = pd.DataFrame(funcVec_b())
            vector_b_Arr = vector_b.to_numpy()

            def funcVec_c():
                vector3 = list()
                for i in range(df.shape[0]):
                    vecHipToFeet = sqrt((xFT[i]-xHT[i])**2+(yFT[i]-yHT[i])**2+(zFT[i]-zHT[i])**2)
                    vector3.append(vecHipToFeet)
                return vector3
            vector_c = pd.DataFrame(funcVec_c())
            vector_c_Arr = vector_c.to_numpy()

            # Abspeichern der Richtungsvektoren a, b, c in einem Array
            directVectors_3D = (vector_a_Arr, vector_b_Arr, vector_c_Arr)
            return (directVectors_3D)   

        # Berechnung des Kniewinkels
        time_Vicon = df.iloc[:,0]
        directionVEcData = funcDirectionVectors()

        def angleCalc():
            a = directionVEcData[0]
            b = directionVEcData[1]
            c = directionVEcData[2]

            angles = list()
            for i in range (df.shape[0]):
                angle_trials = (acos((a[i]**2 + b[i]**2 - c[i]**2)/(2*a[i]*b[i])))
                angles.append(angle_trials)
            return angles

        result = pd.DataFrame(angleCalc())
        resultArr = result.to_numpy()

        # Umwandlung Bogenmaß in Degree 
        angleList = list()
        for i in resultArr:
            i = math.degrees((i))
            angleList.append(i)

        # Abspeichern der Figures und Winkelberechnungen
        LH_P = None
        if lighthouse_Pos == 1:
            LH_P = "LH_normal"
        elif lighthouse_Pos == 2:
            LH_P = "LH_special"

        # Zeit- und Winkelveränderungen plotten
        colors = ("black","green","blue","red")
        style.use('ggplot')
        fig, ax = plt.subplots(figsize=(8,6))
        plt.plot(time_Vicon, angleList, linewidth=2, alpha=0.75, color=colors[fig_Name])
        ax.grid(True, color="k")
        plt.title('Angle Time Measurements Vicon System')
        plt.ylabel('Angle in °')
        plt.xlabel('Time in Frames')
        plt.ylim(50,150)
        plt.savefig('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Vicon\\'+LH_P+'\\Figures\\'+str(hertz)+'Hz'+str(rpm)+'Rpm\\Figures' + str(fig_Name) + "_" + str(mode) + '.png', dpi=300, bbox_inches='tight')
        #plt.show()

        # Excel Tabelle schreiben
        col1 = "Time"
        col2= "Angles"
        angleList = pd.DataFrame(angleList)
        dataAngles = pd.DataFrame({col1:time_Vicon,col2:angleList[0]})
        dataAngles.to_csv('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\\Vicon\\'+LH_P+'\\AngleData\\'+str(hertz)+'Hz'+str(rpm)+'Rpm\\AngleData' + str(fig_Name) + "_" + str(mode) + '.csv')
        angleCalc()

    wholeCalculation(df, fig_Name, mode, lighthouse_Pos)

    def repWC_special():
        df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\Vicon\\"+str(hertz)+"Hz_"+str(rpm)+"rpm_0" + str(excelSheet) + "_s.csv", sep=";", skiprows=4, encoding='latin1')
        mode = 2
        lighthouse_Pos = 2
        wholeCalculation(df, fig_Name, mode, lighthouse_Pos)
    repWC_special()

    for i in range(0,2,1):
        excelSheet += 1
        fig_Name += 1
        def repWC_normal():
            df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\Vicon\\"+str(hertz)+"Hz_"+str(rpm)+"rpm_0" + str(excelSheet) + ".csv", sep=";", skiprows=4, encoding='latin1')
            wholeCalculation(df, fig_Name, mode, lighthouse_Pos)
        repWC_normal()

        def repWC_special():
            df = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Rohdaten\Vicon\\"+str(hertz)+"Hz_"+str(rpm)+"rpm_0" + str(excelSheet) + "_s.csv", sep=";", skiprows=4, encoding='latin1')
            mode = 2
            lighthouse_Pos = 2
            wholeCalculation(df, fig_Name, mode, lighthouse_Pos)
        repWC_special()

mult_Excel(excelSheet, mode, lighthouse_Pos, hertz, rpm)