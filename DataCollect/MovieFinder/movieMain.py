import os
import json
import pandas as pd

import gzip
import shutil
import urllib.request

def createFolder(folder):
    "create a folder"
    if not os.path.exists(folder): 
        os.makedirs(folder) 


def getDataset():
    "get the wanted dataset from url and extract it"
    urllib.request.urlretrieve("https://datasets.imdbws.com/title.akas.tsv.gz", "MovieFinder/data/title.akas.tsv.gz")
    with gzip.open("MovieFinder/data/title.akas.tsv.gz", 'rb') as f_in:
        with open("MovieFinder/data/title.akas.tsv", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def getDictMovies():
    "read the imdb file and extract id, language and movie for each entry"
    data = pd.read_csv("MovieFinder/data/title.akas.tsv",sep="\t")
    dict_movies = {}
    for i,titleId in enumerate(data["titleId"]):
        if titleId not in dict_movies:
            dict_movies[titleId] = {}
        if data["language"][i] not in dict_movies[titleId]:
            dict_movies[titleId][data["language"][i]] = data["title"][i]
    with open('MovieFinder/data/dict_movies.json', 'w',encoding="utf'8") as f:
        json.dump(dict_movies, f, indent=4, ensure_ascii=False)
    

def getLanguagesNumber(dict_movies):
    "allows us to count the number of languages in this dataset"
    languages = set()
    for titleId, lang in dict_movies.items():
        for k in lang.keys():
            languages.add(k)
    return len(languages)-1 # -1 to take into account the NULL value


def applyTag():
    "apply a simple tag to indicate from which dataset each title come from"
    with open("MovieFinder/data/dict_movies.json",'r',encoding="utf-8") as f:
        dict_movies = json.load(f)
    for k,v in dict_movies.items():
        v["origin"] = "movie"
    with open('MovieFinder/data/dict_movies.json', 'w',encoding="utf'8") as f:
        json.dump(dict_movies, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    createFolder("MovieFinder/data")
    if not os.path.exists("MovieFinder/data/title.akas.tsv"):
        getDataset()
        1/0

    if not os.path.exists("MovieFinder/data/dict_movies.json"):
        print("getting titles... (this might takes a while !)")
        getDictMovies()
        applyTag()
        print("titles saved in PressFinder/data/dict_movies.json !")

    print("getting some basic metadata...")
    with open("MovieFinder/data/dict_movies.json",'r',encoding="utf-8") as f:
        dict_movies = json.load(f)
    print(f"number of titles : {len(dict_movies.keys())}")
    print(f"number of languages : {getLanguagesNumber(dict_movies)}")
    print("done !")
