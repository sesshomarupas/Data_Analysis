#In[]
import pandas as pd
import numpy as np
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
cf.go_offline()

# Installation = pip install nbformat, pip install cufflinks, pip install plotly

df = pd.DataFrame(np.random.randn(100,4), columns="A B C D".split())
df2 = pd.DataFrame({"Kategorie":["A","B","C"],"Werte":[32,43,50]})
df3 = pd.DataFrame({"X":[1,2,3,4,5],"Y":[10,20,30,20,10],"Z":[5,4,3,2,1]})

#In[] Plot-Funktion
df[["A","B"]].plot()
#In[] iPlot-Funktion
df[["A","B"]].iplot()
#In[] Scatter
df.iplot(kind="scatter", x="A",y="B", mode="markers", size=10)
#In[] Bar Plots
df2.iplot(kind="bar", x="Kategorie",y="Werte")
#In[]Anzahl
df.count().iplot(kind="bar")
#In[] Boxplot
df.iplot(kind="box")
#In[] 3D Grafiken
df3.iplot(kind="surface", colorscale="rdylbu")
#In[] SpreadPlot
df[["A","B"]].iplot(kind="spread")
#In[] Histogramm
df["A"].iplot(kind="hist",bins=25)
#In[] Bubble
df.iplot(kind="bubble", x="A",y="B", size="C")
#In[] Scatter Matrix
df.scatter_matrix()
# %%
