#In[] While-Schleifen Prinzip und Wärmer oder Kälter Spiel
import random
import pandas as pd
k = int(random.uniform(1,100))
result_table = []
result_description = []

def gameCoffee(k, result_table, result_description):
    geheimzahl = k
    name = str(input("Bitte geben Sie Ihren Namen ein: "))
    eingabeUser = int(input("Finden Sie die Zahl zwischen 1 und 100; Geben Sie nun eine Zahl ein: "))
    distance_one = abs(geheimzahl-eingabeUser)
    versuch = 1
    target_hit = False
    
    def warmOderKalt(eingabeUser, distance_one, versuch, target_hit, name, result_table, result_description):
        print("Leider nicht richtig. Probieren Sie es erneut!")
        while eingabeUser != geheimzahl and versuch <= 30 and target_hit == False:
            versuch += 1
            eingabeUser = int(input("Geben Sie eine Zahl ein: "))
            distance_two = abs(geheimzahl - eingabeUser)
            if  eingabeUser == geheimzahl:
                target_hit == True
                print("Das war die richtige Zahl! Benötigte Versuche: ", versuch)
                result_table.append(pd.DataFrame({"{}".format(name): versuch}, index = [0]))
                result_description.append({"{}".format(name): versuch})
            if versuch > 30:
                print("Maximale Anzahl an Versuchen erreicht")
            if distance_two > distance_one:
                print("kalt")
            elif distance_two == distance_one:
                print("Das war die gleiche Zahl")
            elif distance_two < distance_one and target_hit == False:
                print("warm")
            distance_one = abs(geheimzahl-eingabeUser)
    warmOderKalt(eingabeUser, distance_one, versuch, target_hit, name, result_table, result_description)

gameCoffee(k, result_table, result_description)

for i in range(1, 3, 1):
    k = int(random.uniform(1,100))
    gameCoffee(k, result_table, result_description)

print("Das Ergebnis lautet: ", result_description)
pd.concat(result_table, axis = 1).to_csv("results.csv")