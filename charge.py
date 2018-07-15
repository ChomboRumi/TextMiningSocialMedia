# coding=utf-8

import json
import csv
import re


def rellenarLabel(dataset,label):
    dataset.append(label)
    return dataset

def generateBoW(frases,numeroPalabras):

    for frase in frases:
        string=normalize(frase)
        bol=re.sub("[^a-z]"," ",string).split(" ")
        for word in bol:
            if len(word) <1:
                continue
            elif numeroPalabras.get(word) == None:
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
    for i in sorted(dict2.keys(), reverse=True):
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

def vectoritacio(frases,vocabulari):
    fra=[]
    for frase in frases:
        string=normalize(frase)
        bol= string.split(" ")
        bolLocal={}
        vector=[]
        for word in bol:
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
with open("truthTest.txt", 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=':')
    for row in spamreader:
        dic = {}
        if len(row) > 1:
            dic["sexo"]=row[3]
            dic["nacionalidad"]=row[6]
            dicId[row[0]] = dic
dicIdTrain = {}
with open("truth.txt", 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=':')
    for row in spamreader:
        dic = {}
        if len(row) > 1:
            dic["sexo"]=row[3]
            dic["nacionalidad"]=row[6]
            dicIdTrain[row[0]] = dic







vocabularioNacional = {}
vocabularioNacionalTest = {}

with open("frases_training.json") as json_data:
    data = json.load(json_data)
    lexicon={}
    for id in data.keys():
        lexicon=generateBoW(data[id],lexicon)
    bolsaPalabras=reduceBow(lexicon,500)

with open('bagOfWords.json', 'w') as outfile:
    json.dump(bolsaPalabras, outfile)






