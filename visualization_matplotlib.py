#In[]
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.style.use('_mpl-gallery')
df_csv = pd.read_csv("90Hz_80rpm_01.csv",delimiter =";",decimal=".", skiprows=4)
data = pd.DataFrame(df_csv)
xs = data.iloc[:,2]
ys = data.iloc[:,3]
zs = data.iloc[:,4]

#In[] 2d Modelle
plt.plot(xs,ys, 'red')
plt.xlabel('X Achse')
plt.ylabel('Y Achse')
plt.title('Bewegungskoordinaten')

#In[] Subplots Mehrere Diagramme in einem Diagramm
plt.subplot(1,3,1) # 1 = Anzahl der Zeilen, 2 = Anzahl der Spalten, 1 = Nummer der Grafik
plt.plot(xs,ys,'r--')
plt.subplot(1,3,2)
plt.plot(ys,zs, 'g*-')
plt.subplot(1,3,3)
plt.plot(zs,ys,'b--')

#In[] Objektorientierte Arbeitsfläche
af = plt.figure()
axes = af.add_axes([0.1, 0.5, 0.8, 0.8]) # Position Links unten, Position unten, Breite, Höhe)
axes.plot(xs,ys,'b')
axes.set_xlabel("X Label")
axes.set_ylabel("Y Label")
axes.set_title('Überschrift')

#In[] Obj, Achsendefinitionen
af = plt.figure()
axes1 = af.add_axes([0.1, 0.1, 0.8, 0.8])
axes2 = af.add_axes([0.9, 0.6, 0.5, 0.3])

axes1.plot(xs,ys,'b')
axes1.set_xlabel("X")
axes1.set_ylabel("Y")
axes1.set_title("GROSSE")

axes2.plot(ys,xs,'r')
axes2.set_xlabel("X")
axes2.set_ylabel("Y")
axes2.set_title("KLEINE")

#In[] Subplots
diag, axes = plt.subplots(nrows = 1, ncols=2)

for ax in axes: 
    axes[0].plot(xs,ys,'b')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    axes[1].plot(zs,ys,'r')
    ax.set_title('Titel')

plt.tight_layout() # Ohne Überschneidung

#In[] Diagramm-Größe
diag = plt.figure(figsize=(8,4),dpi=300)
ax = diag.add_axes([0,0,1,1])
ax.plot(xs,ys)

#In[] Größe ändern Subplots
diag, axes = plt.subplots(figsize=(12,3))
axes.plot(xs,ys)
ax.set_title("Titel")
diag.savefig("dateiname.png",dpi=300)

#In[]
diag = plt.figure()
ax = diag.add_axes([0,0,1,1])
ax.plot(xs, ys, label = "y")
ax.plot(ys, xs, label = "x")
ax.legend(loc=0) # Position der Legende
plt.show()

#In[] Farbe, Typ einer Linie
diag, ax = plt.subplots()
# ax.plot(xs, ys, 'b-') # Punkte .-, gestrichelte Linie: --, doppel Punkt :
ax.plot(xs,ys, color="blue", alpha=0.9, linewidth=0.6, linestyle='--', 
marker='o',markersize=5, markerfacecolor="black", 
markeredgewidth = 3, markeredgecolor = "purple") # durchsichtiger Graph, RGB Hex Code #FF1C00, linestyle = steps

#In[] Diagramm zuschneiden
diag, ax = plt.subplots()
ax.plot(xs,ys, color="blue")
ax.set_ylim([500,750])
ax.set_xlim([-900,-300])
plt.show()
