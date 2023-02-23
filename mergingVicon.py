#In[]
import os 
import numpy as np
import pandas as pd
pathVicon = "C:\\Users\\49176\\Desktop\\Vicon\\data\\"

listPathwayVicon = []

for entry in os.listdir(pathVicon):
    listPathwayVicon.append(entry)

listDict = []
num = 0

def createDataFrames(num):
    data = pd.DataFrame(pd.read_csv(pathVicon+listPathwayVicon[num]))
    listDict.append(pd.DataFrame({"number": data.iloc[:,0], "Outliers "+ listPathwayVicon[num][:13] + "_" + listPathwayVicon[num][27:36]: data.iloc[:,1]}, index=range(1,int(len(data)))))

createDataFrames(num)

for i in range(1, len(listPathwayVicon), 1):
    num+=1
    createDataFrames(num)

endDataFrame = pd.concat(listDict, axis=1)
endDataFrame.to_csv("Vicon_Outliers.csv")
# %%
