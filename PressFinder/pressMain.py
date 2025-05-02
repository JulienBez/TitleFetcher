# you have to download the corpus firsthand here : https://www.kaggle.com/datasets/felixludos/babel-briefings
# simply put it in data/ and run this script

import os
import json
import glob

def createFolder(folder):
    "create a folder"
    if not os.path.exists(folder): 
        os.makedirs(folder) 


def getLanguagesNumber(dict_press):
    "allows us to count the number of languages for one file"
    languages = set()
    for key,value in dict_press.items():
        languages.add(value["language"].lower())
    return languages


def getMetadata():
    "check all json files one by one to collect metadatas"
    total_lang = set()
    size = 0
    for path in glob.glob("data/split/*.json"):
        with open(path,'r',encoding="utf-8") as f:
            dict_press = json.load(f)
        lang = getLanguagesNumber(dict_press)
        total_lang.update(lang)
        size += len(dict_press.keys())
    return len(total_lang), size


def getDictPress():
    "reads the corpus file and extract id, language and title for each press article"
    "saves titles in X json files, each containing up to 200.000 titles"

    dict_press = {}
    counter = 0
    file_counter = 0

    for path in glob.glob("data/babel-briefings-v1-anon/*.json"): 

        with open(path,'r',encoding="utf-8") as f:
            data = json.load(f)  

        for entry in data:

            if entry["ID"] not in dict_press:
                dict_press[entry["ID"]] = {"title":entry["title"],"language":entry["language"],"origin":"press"}

            counter += 1

            if counter == 200000:

                with open(f'data/split/press_{file_counter}.json', 'w',encoding="utf'8") as f:
                    json.dump(dict_press, f, indent=4, ensure_ascii=False)

                counter = 0
                dict_press = {}
                file_counter += 1


if __name__ == "__main__":

    createFolder("data/split")

    if len(os.listdir("data/split")) == 0:
        print("getting titles... (this might takes a while !)")
        getDictPress()
        print("titles saved in data/split !")

    print("getting some basic metadata...")
    nb_lang, size = getMetadata()
    print(f"number of titles : {size}")
    print(f"number of languages : {nb_lang}")
    print("no titles with unreferenced language values") #we didn't find any while looking at the corpus
    print("done !")
