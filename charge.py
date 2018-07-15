# coding=utf-8

import json
import csv
import re
import pickle

import nltk
from nltk.tag import hmm
from nltk.tag import tnt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import math

def normalize(frase):
    string = frase.lower()
    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[èéêë]", 'e', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[ýÿ]", 'y', string)
    return string


def rellenarLabel(dataset,label):
    dataset.append(label)
    return dataset

def generateBoW(frases,numeroPalabras,bw):

    for frase in frases:
        string=normalize(frase)
        bol=re.sub("[^a-z]"," ",string).split(" ")
        for word in bol:
                if numeroPalabras.get(word) == None:
                      numeroPalabras[word]=1
                else:
                      numeroPalabras[word] = numeroPalabras[word]+1
    return numeroPalabras
def reduceBow(numeroPalabras,n):
    result={}
    dict2={}
    count=0
    for i in numeroPalabras.keys():
        if dict2.get(numeroPalabras[i]) == None:
                dict2[numeroPalabras[i]]=[]
                dict2[numeroPalabras[i]].append(i)
        else:
                dict2[numeroPalabras[i]].append(i)
    for i in sorted(dict2.keys()):
        if count > n :
                break
        for x in dict2[i]:
                if count < 10:
                    print(x)
                result[x]=i
                count = count+1
                if count > n :
                      break
    return dict2

dicId = {}
bolsaPalabras={}
with open("/home/ramon/Escritorio/text/pan-ap17-bigdata/test/truth.txt", 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=':')
    for row in spamreader:
        dic = {}
        if len(row) > 1:
            dic["sexo"]=row[3]
            dic["nacionalidad"]=row[6]
            dicId[row[0]] = dic
dicIdTrain = {}
with open("/home/ramon/Escritorio/text/pan-ap17-bigdata/training/truth.txt", 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=':')
    for row in spamreader:
        dic = {}
        if len(row) > 1:
            dic["sexo"]=row[3]
            dic["nacionalidad"]=row[6]
            dicIdTrain[row[0]] = dic

vocabularioNacional = {}
vocabularioNacionalTest = {}
fileObject = open("tntTrained",'rb')
b = pickle.load(fileObject)
with open("/home/ramon/Escritorio/text/frases_training.json") as json_data:
    data = json.load(json_data)
    lexicon={}
    for id in data.keys():
        lexicon=generateBoW(data[id],lexicon,b)
    bolsaPalabras=reduceBow(lexicon,500)


dicRepeticionesNumeroDePalabras={}
for i in sorted(bolsaPalabras.keys()):
      dicRepeticionesNumeroDePalabras[math.log( i )]=math.log(len(bolsaPalabras[i]))
pdf = pd.DataFrame(list(dicRepeticionesNumeroDePalabras.items()), columns=["repeticiones","numeroP"])
print(dicRepeticionesNumeroDePalabras)

plt.plot(pdf['repeticiones'],pdf['numeroP'])
plt.show() # Depending on whether you use IPython or interactive mode, etc.

