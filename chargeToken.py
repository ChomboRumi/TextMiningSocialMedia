# coding=utf-8

import json
import csv
import re
import pickle

import nltk
from nltk.tag import hmm
from nltk.tag import tnt




def rellenarLabel(dataset,label):
    dataset.append(label)
    return dataset

def generateBoW(frases,numeroPalabras,bw):

    for frase in frases:
        string=normalize(frase)
        bol=re.sub("[^a-z]"," ",string).split(" ")
        for word1 in bol:
            word2=bw.tag(word1)
            if len(word2 )> 1:
                word=word2[1]
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
                result[x]=i
                count = count+1
                if count > n :
                      break
    print(len(result))
    return result

def normalize(frase):
    string = frase.lower()
    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[èéêë]", 'e', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[ýÿ]", 'y', string)
    return string

def vectoritacio(frases,vocabulari,bw):
    fra=[]
    for frase in frases:
        string=normalize(frase)
        bol= string.split(" ")
        bolLocal={}
        vector=[]
        for word1 in bol:
            word=bw.tag(word1)
            if bolLocal.get(word) == None:
                bolLocal[word]=1
            else:
                bolLocal[word] = bolLocal[word]+1
        for word in vocabulari.keys():
            if bolLocal.get(word) != None:
                vector.append(str(bolLocal[word]/vocabulari[word]))
            else:
                vector.append(str(0))
        fra.append(vector)

    return fra



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
    for id in data.keys():
        v=vectoritacio(data[id],lexicon,b)
        vocabularioNacional[id]=v
        vocabularioNacional[id]=rellenarLabel(vocabularioNacional[id],dicIdTrain[id]["nacionalidad"])


with open("/home/ramon/Escritorio/text/frases_test.json") as json_data:
    data = json.load(json_data)
    for id in data.keys():
       dicId[id]["frases"]=data[id]
       v = vectoritacio(data[id], bolsaPalabras,b)
       vocabularioNacionalTest[id] = v
       vocabularioNacionalTest[id] = rellenarLabel(vocabularioNacionalTest[id],dicId[id]["nacionalidad"])


with open('Train.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                             quoting=csv.QUOTE_NONE)
    d = []
    d.append(dic)
    for dic in vocabularioNacional.keys():
        spamwriter.writerow(d + vocabularioNacional[dic])


with open('Test.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                             quoting=csv.QUOTE_NONE)
    d = []
    d.append(dic)
    for dic in vocabularioNacionalTest.keys():
        spamwriter.writerow(d + vocabularioNacionalTest[dic])






