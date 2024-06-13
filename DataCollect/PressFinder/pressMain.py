# you have to download the corpus firsthand here : https://www.kaggle.com/datasets/felixludos/babel-briefings
# simply put it in data/ and run this script

import os
import json
import glob

def getLanguagesNumber(dict_movies):
    "allows us to count the number of languages in this dataset"
    languages = set()
    for titleId, regions in dict_movies.items():
        for k in regions.keys():
            languages.add(k)
    return len(languages)


def getDictPress():
    dict_press = {}
    for path in glob.glob("PressFinder/data/babel-briefings-v1-anon/*.json"): 
        with open(path,'r',encoding="utf-8") as f:
            data = json.load(f)  
        for entry in data:
            if entry["ID"] not in dict_press:
                dict_press[entry["ID"]] = {}
            if entry["language"] not in dict_press[entry["ID"]]:
                dict_press[entry["ID"]][entry["language"]] = entry["title"]
    with open('PressFinder/data/dict_press.json', 'w',encoding="utf'8") as f:
        json.dump(dict_press, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    if not os.path.exists("PressFinder/data/dict_press.json"):
        print("getting titles... (this might takes a while !)")
        getDictPress()
        print("titles saved in PressFinder/data/dict_press.json !")

    print("getting some basic metadata...")
    with open("PressFinder/data/dict_press.json",'r',encoding="utf-8") as f:
        dict_press = json.load(f)
    print(f"number of titles : {len(dict_press.keys())}")
    print(f"number of languages : {getLanguagesNumber(dict_press)}")
    print("done !")
