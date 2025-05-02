import os
import json
import glob
import pandas as pd
from tqdm import tqdm
from io import StringIO
from ftlangdetect import detect # pip install fasttext-langdetect

import gzip
import shutil
import urllib.request

import re
episode_identifier1 = re.compile(r"#\d+\.\d")
episode_identifier2 = re.compile(r"\d*\.?\d* ?(E|e)pisode ?\d*\.?\d*")
episode_identifier3 = re.compile(r"\d*\.?\d* ?EPISODE ?\d*\.?\d*")

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


def isInvalid(errors,title,titleId):
    "check if title is invalid, aka if a row is malformated"
    if "\ntt" in title:
        errors.append(f"{titleId}\t1\t{title}")
        return True
    return False


def isEpisode(episodes,title):
    "check if title is an episode"
    if any(("Episode dated" in title, "Episode #" in title, episode_identifier1.search(title), episode_identifier2.search(title), episode_identifier3.search(title))):
        episodes.append(title)
        return True
    return False


def getLanguage(invalid_languages,title,language):
    "get the most probable language for a given title"
    try:
        guess = detect(text=str(title).replace("\n",""), low_memory=False)
        return guess["lang"]
    except:
        invalid_languages.append(language)
        return "\\N"


def getDictMovies(data,file_counter=0):
    "reads the imdb file and extract id, language and title for each movie"
    "saves titles in X json files, each containing up to 200.000 titles"
    "takes care of duplicates by looking at titles IDs and exact match"
    "retrieve invalid rows to try to fix them"
    "drop episodes numbers from the dataset"

    headers = "\t".join(list(data.columns.values))

    dict_movies = {}
    invalid_list = [headers]
    episode_list = []
    invalid_languages = []
    bannedID = ""
    counter = 0

    for i,titleId in enumerate(tqdm(data["titleId"])):

        title = str(data["title"][i])
        invalid = isInvalid(invalid_list,title,titleId)
        episode = isEpisode(episode_list,title)

        if titleId != bannedID:

            if invalid or episode:
                bannedID = titleId

            else:

                language = data["language"][i]
                dict_movies[f"{titleId}_{counter}"] = {"title":title,"language":language,"origin":"movie"}

                if language == "\\N":
                    dict_movies[f"{titleId}_{counter}"]["language"] = getLanguage(invalid_languages,title,language)

                counter += 1

                if counter == 200000:

                    with open(f'data/split/movies_{file_counter}.json', 'w',encoding="utf'8") as f:
                        json.dump(dict_movies, f, indent=4, ensure_ascii=False)
                        
                    file_counter += 1
                    counter = 0
                    dict_movies = {}
    
    with open(f'data/split/movies_{file_counter}.json', 'w',encoding="utf'8") as f:
        json.dump(dict_movies, f, indent=4, ensure_ascii=False)

    if os.path.isfile("data/episodes.json"):
        with open("data/episodes.json","r",encoding="utf-8") as f:
            old_episode_list = json.load(f)
        episode_list = old_episode_list + episode_list

    with open("data/episodes.json","w",encoding="utf-8") as f:
        json.dump(episode_list, f, indent=4, ensure_ascii=False)

    if os.path.isfile("data/invalid_languages.json"):
        with open("data/invalid_languages.json","r",encoding="utf-8") as f:
            old_invalid_languages = json.load(f)
        invalid_languages = old_invalid_languages + invalid_languages

    with open("data/invalid_languages.json","w",encoding="utf-8") as f:
        json.dump(list(set(invalid_languages)), f, indent=4, ensure_ascii=False)

    return file_counter+1, "\n".join(invalid_list)
    

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


def getEpisodeFreq():
    "returns the total number of titles dropped for corresponding to episodes"
    with open("data/episodes.json","r",encoding="utf-8") as f:
        episode_list = json.load(f)
    return len(episode_list)


if __name__ == "__main__":

    createFolder("data")
    createFolder("data/split")

    if not os.path.exists("data/title.akas.tsv"):
        print("downloading the dataset...")
        getDataset()

    if len(os.listdir("data/split")) == 0:
        print("getting titles... (this might takes a while !)")
        data = pd.read_csv("data/title.akas.tsv",sep="\t")
        file_counter, invalids = getDictMovies(data)
        invalids = pd.read_csv(StringIO(invalids),sep="\t").fillna("\\N")
        getDictMovies(invalids,file_counter=file_counter)
        print("titles saved in data/split !")

    print("getting some basic metadata...")
    nb_lang, nb_null, size = getMetadata()
    nb_episode = getEpisodeFreq()
    print(f"number of titles : {size}")
    print(f"number of languages : {nb_lang}")
    print(f"number of unreferenced language values : {nb_null}")
    print(f"number of dropped titles corresponding to episodes numbers : {nb_episode}")
    print("done !")

