#In[]
import random
x = 5; y = 9; z = 10
# If-Anweisung plus Befehl in einer Zeile
if x == 4: print("Funktioniert")
# Variable zuordnen, falls Bedingung zutrifft
var = (20 if x == 4 else 30)

list_of_dictionaries = [{"Stefan": 6}, {"Alexander": 7}, {"Dan": 5}]
points_Proband_1 = int(str(list_of_dictionaries[0].values())[-5:][2:3])
points_Proband_2 = int(str(list_of_dictionaries[1].values())[-5:][2:3])
points_Proband_3 = int(str(list_of_dictionaries[2].values())[-5:][2:3])
#In[] Inhalt jeder Zeile in einen Dictionary speichern
woerter = {}
fobj = open("woerterbuch.txt", "r")
for line in fobj:
    line = line.strip()
    zurodnung = line.split()
    woerter[zurodnung[0]] = zurodnung[1]
fobj.close()
while True:
    wort = input("Geben Sie ein Wort ein: ")
    if wort in woerter:
        print("Das deutsche Wort lautet: ", woerter[wort])
    else:
        print("Das Wort ist unbekannt")

#In[] PNG einlesen, Beite, Höhe, Farbtiefe bestimmen
def bytes2int(b):
    res = 0
    for x in b[::-1]:
        res = (res << 8) + x
    return res
f = open("fifth.bmp", "rb")
f.seek(18)
print("Breite:", bytes2int(f.read(4)), "px")
print("Höhe:", bytes2int(f.read(4)), "px")
f.seek(2,1)
print("Farbtiefe:", bytes2int(f.read(2)), "bpp")
f.close()
# %%
