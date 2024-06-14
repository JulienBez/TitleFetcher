import os
import json
import glob
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
    urllib.request.urlretrieve("https://datasets.imdbws.com/title.akas.tsv.gz", "data/title.akas.tsv.gz")
    with gzip.open("data/title.akas.tsv.gz", 'rb') as f_in:
        with open("data/title.akas.tsv", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def getDictMovies():
    "reads the imdb file and extract id, language and title for each movie"
    "saves titles in X json files, each containing up to 200.000 titles"
    "takes care of duplicates by looking at titles IDs and exact match"

    data = pd.read_csv("data/title.akas.tsv",sep="\t")
    dict_movies = {}

    counter = 0
    file_counter = 0

    previous_title = []
    previous_titleId = data["titleId"][0]

    for i,titleId in enumerate(data["titleId"]):

        if titleId != previous_titleId:
            previous_title = []

        title = data["title"][i]

        if titleId+str(i) not in dict_movies and title not in previous_title:

            dict_movies[titleId+str(i)] = {"title":title,"language":data["language"][i],"origin":"movie"}
            previous_title.append(title)

        counter += 1

        if counter == 200000:

            with open(f'data/split/movies_{file_counter}.json', 'w',encoding="utf'8") as f:
                json.dump(dict_movies, f, indent=4, ensure_ascii=False)
                
            file_counter += 1
            counter = 0
            dict_movies = {}

        previous_titleId = titleId
    

def getLanguagesNumber(dict_movies):
    "allows us to count the number of languages for one file"
    languages = set()
    counter_null = 0
    for key,value in dict_movies.items():
        if value["language"] == "\\N":
            counter_null += 1
        else:
            languages.add(value["language"].lower())
    return languages, counter_null


def getMetadata():
    "check all json files one by one to collect metadatas"
    total_lang = set()
    total_null = 0
    size = 0
    for path in glob.glob("data/split/*.json"):
        with open(path,'r',encoding="utf-8") as f:
            dict_movies = json.load(f)
        lang, nb_null = getLanguagesNumber(dict_movies)
        total_lang.update(lang)
        total_null += nb_null
        size += len(dict_movies.keys())
    return len(total_lang), total_null, size


if __name__ == "__main__":

    createFolder("data")
    createFolder("data/split")

    if not os.path.exists("data/title.akas.tsv"):
        getDataset()

    if len(os.listdir("data/split")) == 0:
        print("getting titles... (this might takes a while !)")
        getDictMovies()
        print("titles saved in data/split !")

    print("getting some basic metadata...")
    nb_lang, nb_null, size = getMetadata()
    print(f"number of titles : {size}")
    print(f"number of languages : {nb_lang}")
    print(f"number of unreferenced language values : {nb_null}")
    print("done !")
