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
    urllib.request.urlretrieve("https://datasets.imdbws.com/title.akas.tsv.gz", "data/title.akas.tsv.gz")
    with gzip.open("data/title.akas.tsv.gz", 'rb') as f_in:
        with open("data/title.akas.tsv", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def getDictMovies():
    "read the imdb file and extract id, language and movie for each entry"

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
    "allows us to count the number of languages in this dataset"
    languages = set()
    for titleId, lang in dict_movies.items():
        for k in lang.keys():
            languages.add(k)
    return len(languages)-1 # -1 to take into account the NULL value


if __name__ == "__main__":

    createFolder("data")
    createFolder("data/split")

    if not os.path.exists("data/title.akas.tsv"):
        getDataset()

    if not os.path.exists("data/dict_movies.json"):
        print("getting titles... (this might takes a while !)")
        getDictMovies()
        print("titles saved in data/dict_movies.json !")

    print("getting some basic metadata...")
    with open("data/dict_movies.json",'r',encoding="utf-8") as f:
        dict_movies = json.load(f)
    print(f"number of titles : {len(dict_movies.keys())}")
    print(f"number of languages : {getLanguagesNumber(dict_movies)}")
    print("done !")
