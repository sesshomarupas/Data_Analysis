#In[]
import numpy as np
import pandas as pd
import math
from math import acos
from math import sqrt
import statistics
import matplotlib.pyplot as plt
from matplotlib import style
from scipy.signal import argrelextrema

# Manuelle Eingabe
frequencyMS = 200
rpm = 80
lightHousePos = 2 # 1 = normal, 2 = special 
# Standardparameter
timeViconModified = []
if frequencyMS == 90:
    hertzVicon = 90.0225
elif frequencyMS == 200:
    hertzVicon = 200
hertzUnity = 90
dataCount = 1
figNum = 1
specialMode = None
if lightHousePos ==2:
    specialMode = 2
elif lightHousePos ==1:
    specialMode = 1

def com_Systems(dataCount, hertzUnity, hertzVicon, lightHousePos, figNum, timeViconModified):
    
    folderName = None
    if lightHousePos == 1:
        folderName = "LH_normal"
    elif lightHousePos == 2:
        folderName = "LH_special"

    df_Vicon = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Vicon\\"+folderName+"\\"+str(frequencyMS)+"Hz"+str(rpm)+"Rpm\\AngleData"+str(dataCount)+"_"+str(specialMode)+".csv", sep=",", decimal=".", skiprows=1, encoding='latin1')
    df_Unity = pd.read_csv("C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Unity\\"+folderName+"\\"+str(frequencyMS)+"Hz"+str(rpm)+"Rpm\\AngleData"+str(dataCount)+"_"+str(specialMode)+".csv", sep=",", decimal=".", skiprows=1, encoding='latin1')    
    time_Vicon = df_Vicon.iloc[:,1]
    time_Unity = df_Unity.iloc[:,1]
    angle_Vicon = df_Vicon.iloc[:,2]
    angle_Unity = df_Unity.iloc[:,2]
    endTime_Unity = df_Unity.iloc[-1:,1]
    endTime_Vicon = df_Vicon.iloc[-1:,1]

    for i in time_Vicon: 
        newTime = i/hertzVicon
        timeViconModified.append(newTime)

    # Min and Max
    angles_Max_Vicon = np.array(angle_Vicon)[argrelextrema(np.array(angle_Vicon), np.greater)]
    angles_Min_Vicon = np.array(angle_Vicon)[argrelextrema(np.array(angle_Vicon), np.less)]
    angles_Max_Unity = np.array(angle_Unity)[argrelextrema(np.array(angle_Unity), np.greater)]
    angles_Min_Unity = np.array(angle_Unity)[argrelextrema(np.array(angle_Unity), np.less)]

    Vicon_index_maxima = argrelextrema(np.array(angle_Vicon), np.greater)
    Vicon_index_minima = argrelextrema(np.array(angle_Vicon), np.less)
    Unity_index_maxima = argrelextrema(np.array(angle_Unity), np.greater)
    Unity_index_minima = argrelextrema(np.array(angle_Unity), np.less)

    df_Vicon_new = {"Time": timeViconModified, "Angles": angle_Vicon}
    df_Vicon_new_DT = pd.DataFrame(df_Vicon_new)
    plot_Vicon_time_max = df_Vicon.iloc[Vicon_index_maxima[0],1]
    plot_Vicon_time_min = df_Vicon.iloc[Vicon_index_minima[0],1]
    plot_Unity_time_max = df_Unity.iloc[Unity_index_maxima[0],1]
    plot_Unity_time_min = df_Unity.iloc[Unity_index_minima[0],1]

    min_max_Vicon_fig = plt.figure()
    axes = min_max_Vicon_fig.add_axes([0.5,0.1,0.8,0.8])
    axes.plot(plot_Vicon_time_max,angles_Max_Vicon,'red')
    axes.plot(plot_Vicon_time_min,angles_Min_Vicon,'orange')
    axes.set_title('Vicon minima and maxima of the angles')
    axes.set_xlabel("Time")
    axes.set_ylabel("Angles")
    plt.ylim(60,140)
    plt.savefig('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Figures\\'+folderName+'\\'+str(frequencyMS)+'Hz'+str(rpm)+'Rpm\\Figure'+str(figNum)+'Min_Max_Vicon.png', dpi=300, bbox_inches='tight')

    min_max_Unity_fig = plt.figure()
    axes2 = min_max_Unity_fig.add_axes([0.5,0.1,0.8,0.8])
    axes2.plot(plot_Unity_time_max,angles_Max_Unity,'green')
    axes2.plot(plot_Unity_time_min,angles_Min_Unity, 'darkgreen')
    axes2.set_title('Unity minima and maxima of the angles')
    axes2.set_xlabel("Time")
    axes2.set_ylabel("Angles")
    plt.ylim(60,140)
    plt.savefig('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Figures\\'+folderName+'\\'+str(frequencyMS)+'Hz'+str(rpm)+'Rpm\\Figure'+str(figNum)+'Min_Max_Unity.png', dpi=300, bbox_inches='tight')

    lenghts_angles = [[len(angles_Max_Vicon)], [len(angles_Min_Vicon)], [len(angles_Max_Unity)], [len(angles_Min_Unity)]]
    lengthIndex = max((int(len(angles_Max_Vicon))),(int(len(angles_Max_Unity))),(int(len(angles_Min_Vicon))), (int(len(angles_Min_Unity))))
    index_List = []
    for i in range(0,lengthIndex,1):
        index_List.append("index")

    an_Max_Vic = list(angles_Max_Vicon)
    an_Min_Vic = list(angles_Min_Vicon)
    an_Max_Un = list(angles_Max_Unity)
    an_Min_Un = list(angles_Min_Unity)

    def listFill(x,lengthIndex,y):
        if len(x)<=lengthIndex:
            for i in range(0,lengthIndex-len(x),1):
                y.append("NaN")
    
    listFill(angles_Max_Vicon, lengthIndex, an_Max_Vic)
    listFill(angles_Min_Vicon, lengthIndex, an_Min_Vic)
    listFill(angles_Max_Unity, lengthIndex, an_Max_Un)
    listFill(angles_Min_Unity, lengthIndex, an_Min_Un)
    dataSet_Min_Max = pd.DataFrame({"Minima_Vicon": an_Min_Vic, "Minima_Unity": an_Min_Un,"Maxima_Vicon": an_Max_Vic, "Maxima_Unity": an_Max_Un}, index=index_List)
    dataSet_Min_Max.to_csv('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Min_Max\\'+folderName+'\\'+str(frequencyMS)+'Hz'+str(rpm)+'Rpm\\Min_Max'+str(figNum)+'.csv')

    colors = ("black","green")
    style.use('ggplot')
    fig, ax = plt.subplots(figsize=(8,6))
    plt.plot(time_Unity, angle_Unity, linewidth=2, alpha=0.75, color=colors[0])
    plt.plot(timeViconModified, angle_Vicon, linewidth=2, alpha=0.75, color=colors[1])
    ax.grid(True, color="k")
    plt.title('Angle Time Measurements of both Systems')
    plt.ylabel('Angle in °')
    plt.xlabel('Time in Seconds')
    plt.ylim(50,150)
    plt.legend(['Unity','Vicon'])
    plt.savefig('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Figures\\'+folderName+'\\'+str(frequencyMS)+'Hz'+str(rpm)+'Rpm\\Figure'+str(figNum)+'.png', dpi=300, bbox_inches='tight')
    col1 = "Time_Vicon"
    col2= "Angles_Vicon"
    col3 = "Time_Unity"
    col4 = "Angles_Unity"
    data = pd.DataFrame({col1:timeViconModified,col2:angle_Vicon})
    data_2 =pd.DataFrame({col3:time_Unity,col4:angle_Unity})
    df_merged = pd.concat([data,data_2])
    df_merged.to_csv('C:\\Users\\49176\\Desktop\\Python_Scripts\\Angle_Calculation_Unity_Vicon\\Comparison\\Figures\\'+folderName+'\\'+str(frequencyMS)+'Hz'+str(rpm)+'Rpm\\y_and_x'+str(figNum)+'.csv')

com_Systems(dataCount, hertzUnity, hertzVicon, lightHousePos, figNum, timeViconModified)

for i in range(0,2,1):
    dataCount+=1
    figNum+=1
    timeViconModified=[]
    com_Systems(dataCount, hertzUnity, hertzVicon, lightHousePos, figNum, timeViconModified)
# %%
