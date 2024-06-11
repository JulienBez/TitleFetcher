# https://datasets.imdbws.com/
# download title.akas.tsv.gz, extract and run this script on it+

import os
import json
import pandas as pd

def getDictMovies():
    data = pd.read_csv("data/title.akas.tsv",sep="\t")
    dict_movies = {}
    for i,titleId in enumerate(data["titleId"]):
        if titleId not in dict_movies:
            dict_movies[titleId] = {}
        if data["region"][i] not in dict_movies[titleId]:
            dict_movies[titleId][data["region"][i]] = data["title"][i]
    with open('data/dict_movies.json', 'w',encoding="utf'8") as f:
        json.dump(dict_movies, f, indent=4, ensure_ascii=False)
    

def getLanguagesNumber(dict_movies):
    languages = set()
    for titleId, regions in dict_movies.items():
        for k in regions.keys():
            languages.add(k)
    return len(languages)-1 # -1 to take into account the NULL value


if __name__ == "__main__":

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
