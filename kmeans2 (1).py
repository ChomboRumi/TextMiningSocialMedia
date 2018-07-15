import numpy as np  

from random import shuffle
import csv
import re
from sklearn.cluster import KMeans 


llistaTest=[]
labelSexoTest=[]
labelNacionalidadTest=[]
with open('Test.csv', 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
     for row in spamreader:
         id=row[0]
         for i in range(1,len(row)-3):
            listaInterior=[]
            labelSexoTest.append(row[len(row)-1])
            labelNacionalidadTest.append(row[len(row)-2])
            for j in row[i].split(","):
                listaInterior.append(float(re.sub(r'[^0-9]', '',j)))
            llistaTest.append(listaInterior)
			

         
         #print float(re.sub(r'[^0-9]', '',row[1].split(",")[0]))

lista=[]
labelSexo=[]
labelNacionalidad=[]
with open('Train.csv', 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
     for row in spamreader:
         id=row[0]
         for i in range(1,len(row)-3):
             listaInterior=[]
             for j in row[i].split(","):
                 listaInterior.append(float(re.sub(r'[^0-9]', '',j)))
             labelSexo.append(row[len(row)-1])
             labelNacionalidad.append(row[len(row)-2])
             lista.append(listaInterior)


X = np.asarray(lista, dtype=np.float32)
lista=None

kmeans = KMeans(n_clusters=2)  


kmeans.fit(X)
labelCluster={}
numeroLabelsPorCluster={}
for i in range(0,len(X)):
     cluster=kmeans.predict(np.matrix(X[i], dtype=np.float32))[0]
     if numeroLabelsPorCluster.get(cluster)==None:
          numeroLabelsPorCluster[cluster]={}
          numeroLabelsPorCluster[cluster][labelNacionalidad[i]]=1
     elif numeroLabelsPorCluster[cluster].get(labelNacionalidad[i])==None:
          numeroLabelsPorCluster[cluster][labelNacionalidad[i]]=1
     else :
          numeroLabelsPorCluster[cluster][labelNacionalidad[i]]=numeroLabelsPorCluster[cluster][labelSexo[i]]+1
labelSexo=None
contadorId={}
listadoId=[]
clusterLabel={}
for cluster in numeroLabelsPorCluster:
     mayor=0
     for contador in numeroLabelsPorCluster[cluster]:
         listadoId.append(numeroLabelsPorCluster[cluster][contador])
         contadorId[numeroLabelsPorCluster[cluster][contador]]=(cluster,contador)

listadoId.sort(reverse=True)
for i in range(0,len(listadoId)):
    tupla=contadorId[listadoId[i]]
    cluster=tupla[0]
    contador=tupla[1]
    if labelCluster.get(cluster)==None and clusterLabel.get(contador)==None:
        labelCluster[cluster]=contador
        clusterLabel[contador]= cluster
print(labelCluster)

contTrue=0
contFalse=0
Xt = np.asarray(llistaTest, dtype=np.float32)
llistaTest=None
for i in range(0,len(Xt)):
     cluster=kmeans.predict(np.matrix(Xt[i], dtype=np.float32))[0]
     if labelCluster.get(cluster)==labelNacionalidadTest[i]:
         contTrue=contTrue+1
     else:
         contFalse=contFalse+1
print(contFalse)
print(contTrue)
