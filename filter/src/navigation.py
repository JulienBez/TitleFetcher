import os
import time
import json
import glob
import pickle
import shutil
from tqdm import tqdm

def openJson(path):
  "open a json file"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data
  

def writeJson(path,data):
  "create a json file"
  with open(path,"w",encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)


def createFolder(folder):
    "create a folder"
    if not os.path.exists(folder): 
        os.makedirs(folder) 


def removeFolder(folder):
   "remove a folder and its content"
   if os.path.exists(folder):
      shutil.rmtree(folder)


def openVector(path):
  "open a vector save"
  with open(path, 'rb') as file:
    vector = pickle.load(file)
  return vector


def writeVector(path,vector):
  "create a vector save"
  with open(path, 'wb') as file:
    pickle.dump(vector, file)


def getTitles(language,genres):
    "get all titles for a given language and save them in a dict"
    "for each title, save a list of all ids with this title"
    "return a list of titles according to chosen genres"
    "take care of all duplicates but save at least 1 occurrence of a same title per origin"

    createFolder("data/dictionnaries")
    titlePath = f"data/dictionnaries/dict_{language}.json"

    if not os.path.isfile(titlePath):
        titles = {}

        for path in glob.glob(f"data/languages/{language}/*.json"):
            data = openJson(path)

            for key,value in data.items():

                if value["title"] not in titles:
                    titles[value["title"]] = {}

                if value["origin"] not in titles[value["title"]]:
                    titles[value["title"]][value["origin"]] = []

                titles[value["title"]][value["origin"]].append(key)

        titles = [{k:v} for k,v in titles.items()]
        writeJson(titlePath,titles)

    else:
        titles = openJson(titlePath)
    
    # select the list of returned titles according to chosen genres
    # to avoid duplicates but to take into account identical titles with different origins, we add them 1 time by origin
    titles_selection = []
    titles_genres = []
    for dict in titles:
        for title, origins in dict.items():
            for origin, list_id in origins.items():
                if origin in genres:
                    titles_selection.append(title)
                    titles_genres.append(origin)

    return titles_selection, titles_genres


def getVectors(vectorizer,titles,language,genres):
    "vectorize a given list of vectors and save the vectors"
    createFolder("data/vectors")
    createFolder(f"data/vectors/{language}")
    vectorizeName = "".join(x for x in str(vectorizer).replace(" ","_") if x.isalnum() or x == "_")
    Xpath = f"data/vectors/{language}/{language}_{vectorizeName}_{('_'.join(genres))}.vec"
    if not os.path.isfile(Xpath):
        X = vectorizer.fit_transform(titles) # np.array(titles)
        writeVector(Xpath,X)
    else:
        X = openVector(Xpath)
    return X


def getClustersTags(vectorizer,language,genres,titles,clusteType):
  "for each title, retrieve in wich cluster it was found" 
  vectorizeName = "".join(x for x in str(vectorizer).replace(" ","_") if x.isalnum() or x == "_")
  dict_clusters = openJson(f"data/clusters/{language}/{('_').join(genres)}/{clusteType}_{vectorizeName}.json")  
  clusterTags = []
  for title in titles:
      index = [key for key, value in dict_clusters.items() if title in value][0]
      clusterTags.append(index)
  return clusterTags