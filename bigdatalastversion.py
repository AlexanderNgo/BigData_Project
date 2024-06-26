# -*- coding: utf-8 -*-
"""BigDataLastVersion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rxguz15yOYd4imxocSPBrC6rQVF0nEuj
"""

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("CSV_meteo.csv",delimiter = ";")
liste = data["Humidité"].to_list()

#Phase de suppression des colonnes inutile (cf note dans Trello), pas encore toute listés -> ptet encore d'autres à supprimer
#dataWithDeleted = data.drop(["Nébulosité couche nuageuse 3","Nébulosité couche nuageuse 4","Hauteur de base 3","Hauteur de base 4","Température","Variation de pression en 3 heures","Température minimale sur 12 heures","Température minimale sur 24 heures","Température maximale sur 12 heures","Température maximale sur 24 heures","Température minimale du sol sur 12 heures","Température minimale du sol sur 12 heures (en °C)","Température maximale sur 12 heures (°C)","Précipitations dans les 3 dernières heures","Précipitations dans les 6 dernières heures","Précipitations dans les 12 dernières heures","Phénomène spécial 1","Phénomène spécial 2","Phénomène spécial 3","Phénomène spécial 4","Nébulosité couche nuageuse 3","Nébulosité couche nuageuse 4","Hauteur de base 3","Hauteur de base 4"],axis = 1,inplace = True) #inplace permet de supprimé direct dans le df sans faire de copie
#dataWithDeleted = data.drop("Géopotentiel",axis = 1,inplace=True)
liste = data.columns.to_list()
liste1 = ['Précipitations dans la dernière heure','Température maximale sur 12 heures (°C)','Température minimale sur 12 heures (°C)','Phénomène spécial 1','Phénomène spécial 2','Phénomène spécial 3','Phénomène spécial 4','Précipitations dans les 12 dernières heures','Précipitations dans les 3 dernières heures','Précipitations dans les 6 dernières heures','Variation de pression en 3 heures',"Géopotentiel","Température minimale sur 12 heures",'Nébulosité couche nuageuse 3', 'Type nuage 3', 'Hauteur de base 3','Nébulosité couche nuageuse 4', 'Type nuage 4', 'Hauteur de base 4', "Température minimale sur 24 heures", "Température maximale sur 12 heures", "Température maximale sur 24 heures", "Température minimale du sol sur 12 heures", "Température minimale du sol sur 12 heures (en °C)", "Température maximale sur 12 heures (°C)"]

# Supprimer les éléments de liste1 qui ne sont pas présents dans liste
liste1 = [elem for elem in liste1 if elem in liste]
#"Géopotentiel" in liste
#all(elem in liste1 for elems in liste)
dfWithDeleted = data.drop(liste1,axis=1)
#print(data.columns)
dfWithDeleted.head() #on est passé de 82 à 58 colonnes

#fill missing values
columnsWithMissings = dfWithDeleted.columns[dfWithDeleted.isnull().any()]
print(len(columnsWithMissings))
missing_count = dfWithDeleted.isnull().sum()
#print("\nNombre de valeurs manquantes par colonne \n:", missing_count)
colonnes = columnsWithMissings.to_list()
mean = 0
#print(data['communes'].dtype)
colonnes
compteur = 0
for colonne in colonnes:
    if dfWithDeleted[colonne].dtype == "float64":
        compteur += 1
        # Calculer la moyenne des valeurs non NaN dans la colonne
        mean = dfWithDeleted[colonne][pd.notnull(dfWithDeleted[colonne])].mean()

        # Remplacer les valeurs NaN par la moyenne calculée
        dfWithDeleted[colonne].fillna(mean,inplace = True)
    elif dfWithDeleted[colonne].dtype == 'object' :
      dfWithDeleted[colonne].fillna("Inconnu",inplace = True)
      compteur +=1
print(compteur)

#df sans missing values
dfWithDeleted.head()

#Etude des outliers
#Stratégie = utilisé boxplot sur chaque colonne pr détecter outliers puis remplacé les outliers par une valeur médianne dla colonne
fig = plt.figure(figsize=(16,6))
dfWithDeleted["Humidité"].plot(kind = "box")
print(dfWithDeleted["Humidité"].mean)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Copie du DataFrame pour sécuriser
dfCopied = dfWithDeleted.copy()

# Calcul des quartiles et de l'IQR
Q1 = dfCopied["Humidité"].quantile(0.25)
Q3 = dfCopied["Humidité"].quantile(0.75)
IQR = Q3 - Q1

# Calcul des limites des moustaches
limit_Q1 = Q1 - (1.5 * IQR)
limit_Q3 = Q3 + (1.5 * IQR)

# Remplacement des outliers par la moyenne
mean = dfCopied["Humidité"].mean()
dfCopied.loc[(dfCopied["Humidité"] < limit_Q1) | (dfCopied["Humidité"] > limit_Q3), "Humidité"] = mean

# Affichage du boxplot
fig = plt.figure(figsize=(16, 6))
dfCopied["Humidité"].plot(kind="box")
plt.title("Boxplot de la colonne 'Humidité' après traitement des outliers")
plt.show()

#Généraliser ça aux autres colonnes numérique

# Récupérer la liste des colonnes numériques
colonnes_numeriques = dfCopied.select_dtypes(include=['float64']).columns.tolist()

# Parcourir les colonnes numériques
for colonne in colonnes_numeriques:
    # Calcul des quartiles et de l'IQR
    Q1 = dfCopied[colonne].quantile(0.25)
    Q3 = dfCopied[colonne].quantile(0.75)
    IQR = Q3 - Q1

    # Calcul des limites des moustaches
    limite_inf = Q1 - (1.5 * IQR)
    limite_sup = Q3 + (1.5 * IQR)

    # Remplacement des outliers par la moyenne
    moyenne = dfCopied[colonne].mean()
    dfCopied[colonne] = dfCopied[colonne].apply(lambda x: moyenne if x < limite_inf or x > limite_sup else x)

#suppression de la colonne Température en Kelvin
dfCopied.drop("Température",axis = 1,inplace = True)

#afficher les boxplot de chaque colonnes numérique

#compteur = dfCopied.select_dtypes(include = ["float64"]).columns.to_list()
#len(compteur) #donc 45 boxplot à afficher

# Créer une figure avec deux sous-graphiques
fig, axs = plt.subplots(1, 4, figsize=(15, 5))
#Variable c1--c4 à modifier pr voir tous les autres colonnes numérique

# Afficher le boxplot de la colonne "Humidité" dans le premier sous-graphique
c1 = "Altitude"
axs[0].boxplot(dfCopied[c1])
axs[0].set_title(c1)

# Afficher le boxplot de la colonne "Nébulosité des nuages de l'étage inférieur" dans le deuxième sous-graphique
c2 = "Point de rosée"
axs[1].boxplot(dfCopied[c2])
axs[1].set_title(c2)

c3 = "Pression au niveau mer"
axs[2].boxplot(dfCopied[c3])
axs[2].set_title(c3)

c4 = "Type de tendance barométrique"
axs[3].boxplot(dfCopied[c4])
axs[3].set_title(c4)

# Afficher la figure
plt.show()

