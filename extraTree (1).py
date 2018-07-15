import numpy as np  

from random import shuffle
import csv
import re

from sklearn.ensemble import ExtraTreesClassifier


llistaTest=[]
labelSexoTest=[]
labelNacionalidadTest=[]
with open('/home/ramon/Descargas/Test.csv', 'r') as csvfile:
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
with open('/home/ramon/Descargas/Train.csv', 'r') as csvfile:
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



param_grid = { 
    'n_estimators': [100, 200],
    'max_features': ['auto', 'sqrt', 'log2']
}
X = np.asarray(lista, dtype=np.float32)

Y =  np.asarray(labelSexo)
seed = 7
num_trees = 100
max_features = 25
model = ExtraTreesClassifier(n_estimators=num_trees,min_samples_split =0.2, max_features=max_features,random_state=1)


model.fit(X, Y)

XTest = np.asarray(lista, dtype=np.float32)
Ytest =  np.asarray(labelSexoTest)
y_pred=model.predict(XTest)
print(sklearn.metrics.confusion_matrix(Ytest, y_pred))

