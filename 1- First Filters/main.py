import time
from tqdm import tqdm

import json
import glob

from iso639 import Lang # pip install iso639-lang
from ftlangdetect import detect # pip install fasttext-langdetect


################################################################

# FONCTIONS DE BASE #

def openJson(path):
  "open a json file"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data
  
def writeJson(path,data):
  "create a json file"
  with open(path,"w",encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)

################################################################

# QUANTIFIER LES DONNEES #

def getFreqLang():
    "returns a dict with the number of occurrences for each language"
    dict_languages = {}
    for path in tqdm(glob.glob("data/*.json")):
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if value["language"] not in dict_languages:
                dict_languages[value["language"]] = {"language_full":"","total":0}
            dict_languages[value["language"]]["total"] += 1
    writeJson("logs/dict_languages.json",dict(sorted(list(dict_languages.items()), key=lambda item: item[1]['total'], reverse=True)))


def checkLang():
    "check for each ISO language code if it corresponds to a language - allows us to check if our languages metadata are consistent"
    dict_languages = openJson("logs/dict_languages.json")
    less_than_1000 = 0
    error_langues = []
    print("invalid ISO-639-1 language codes :")
    for key,value in dict_languages.items():
        try:
            language_full = Lang(key).name
        except:
            language_full = "NULL"
            print(key, value["total"])
            error_langues.append(key)
        dict_languages[key]["language_full"] = language_full
        if value["total"] < 1000:
            less_than_1000 += 1
    print(f"number of languages with less than 1000 titles : {less_than_1000}")
    writeJson("logs/dict_languages.json",dict_languages)
    writeJson("logs/invalid_languages.json",error_langues)


################################################################

# IDENTIFIER LES LANGUES ET FILTRER PAR LANGUES #

def applyLanguageTag():
    "for each title, identifies its language with fasttext and gives a confidence score"
    " 1 : original tag and identified languages are the same"
    " 0 : original tag is null, we only have the identified language"
    " -1 : original tag and identified languages are not the same"
    " -2 : original tag is an invalid tag"
    null_values = ["\\N","null"]
    excluded = [i for i in openJson("logs/invalid_languages.json") if i not in null_values]
    for path in tqdm(glob.glob("data/*.json")):
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if value["language"] not in excluded:
                guess = detect(text=str(value["title"]).replace("\n",""), low_memory=False)["lang"]
                value["language_confidence"] = -1
                if value["language"] in null_values:
                    value["language_confidence"] = 0
                elif value["language"] == guess:
                    value["language_confidence"] = 1
                value["language"] = guess
            else:
                value["language_confidence"] = -2
        writeJson(path,data)


def getLanguageConfidenceStats(glob_path="data/*.json"):
    "count the number of titles for each possible language_score"
    dict_counter = {"total":0,"1":0,"0":0,"-1":0,"-2":0}
    for path in tqdm(glob.glob(glob_path)):
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key, value in data.items():
            dict_counter[str(value["language_confidence"])] += 1
            dict_counter["total"] += 1
    print(f"# RESULTS FOR {glob_path}")
    print(f"accuracy of the system : {dict_counter['1']/(dict_counter['total']-dict_counter['0']-dict_counter['-2'])}")
    print(dict_counter)


def dropByLanguageConfidence():
    "drops titles whose language_confidence is inferior to 0"
    counter = 0
    for path in tqdm(glob.glob("data/*.json")):
        new_data = {}
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if value["language_confidence"] > 0:
                new_data[key] = value
            else:
                counter += 1
        writeJson(path,new_data)
    print(f"{counter} titles dropped with language_confidence filter")


def dropByLanguageFreq():
    "drops titles whose language has less than 1000 titles" 
    dict_languages = openJson("logs/dict_languages.json")
    counter = 0
    for path in tqdm(glob.glob("data/*.json")):
        new_data = {}
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if dict_languages[value["language"]]["total"] >= 1000:
                new_data[key] = value
            else:
                counter += 1
        writeJson(path,new_data)
    print(f"{counter} titles dropped with language frequency filter")


def dropByLanguage():
    "execute all necessary functions to drop 1) titles with low language_confidence and 2) languages with less than 1 000 titles"
    print("dropping titles with low language_confidence...")
    dropByLanguageConfidence()
    print("recounting occurrences of titles for each languages...")
    getFreqLang()
    print("dropping languages with less than 1,000 titles")
    dropByLanguageFreq()
    print("done !")


#annoter :
# languages erronés (invalid languages) -> les virer ou essayer de les indentifier ?
# languages pas sûrs (les 6M) -> les virer direct ?
# languages très probables (les 40M)
# languages trouvés automatiquement (les nulls)

# titres movies : pas une valeur source, surement des titres de films français écrits en anglais -> langue documentée = fr ou en par imdb ?
# trouver des exemples de ça et expliquer qu'on refait toute l'analyse des langues pour les films

################################################################

if __name__ == "__main__":

    start = time.time()

    #languageIdentifierVSlanguageTags(glob_path="data/*.json")
    #getFreqLang()
    checkLang()
    #applyLanguageTag()
    #getLanguageConfidenceStats()
    #dropByLanguage()

    end = time.time()
    print(f"executed in {round(end - start,2)}")