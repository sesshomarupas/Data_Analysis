#In[]
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mouse

df = pd.read_csv("FinalWithoutStr.csv", delimiter=";")

with open("FinalWithoutStr.csv") as f:
    firstline = f.readlines()[0].rstrip()
    
index_list = list([firstline])

for i in index_list:
    list_new = []
    if ";"in i:
        i = list_new.append(i.split(";",-1))

iterator = 0
dataSet = iterator+1
index_list = list_new[0]
index_list.pop(0)

def figuresPlot(iterator,dataSet):
    x = df.iloc[:,dataSet]
    x_name = index_list[iterator]
    y = df.iloc[:,dataSet+1]
    def kdePLotFig(x,y):
        sns.kdeplot(x)
        sns.kdeplot(y)
        plt.savefig("C:\\Users\\49176\\Desktop\\Python_Scripts\\Visualization_First Trial\\Figures\\Normalverteilung\\"+x_name+".png", dpi=300)
    kdePLotFig(x, y)
figuresPlot(iterator, dataSet)
# %%
