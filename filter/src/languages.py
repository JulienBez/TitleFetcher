from iso639 import Lang # pip install iso639-lang
from ftlangdetect import detect # pip install fasttext-langdetect

from .navigation import *

def getFreqLang():
    "returns a dict with the number of occurrences for each language"
    dict_languages = {}
    for path in tqdm(glob.glob("data/collected/*.json")):
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if value["language"] not in dict_languages:
                dict_languages[value["language"]] = {"language_full":"","total":0}
            dict_languages[value["language"]]["total"] += 1
    writeJson("logs/dict_languages.json",dict(sorted(list(dict_languages.items()), key=lambda item: item[1]['total'], reverse=True)))


def checkLang():
    "returns invalid ISO language codes"
    dict_languages = openJson("logs/dict_languages.json")
    error_langues = []
    for key,value in dict_languages.items():
        try:
            language_full = Lang(key).name
        except:
            language_full = "NULL"
            error_langues.append(key)
        dict_languages[key]["language_full"] = language_full
    writeJson("logs/dict_languages.json",dict_languages)
    writeJson("logs/invalid_languages.json",error_langues)


def applyLanguageTag():
    "for each title, identifies its language with fasttext and gives a language confidence score"
    #  1 : original tag and identified languages are the same
    #  0 : original tag is null, we only have the identified language
    # -1 : original tag and identified languages are not the same
    # -2 : original tag is an invalid tag
    null_values = ["\\N","null"]
    excluded = [i for i in openJson("logs/invalid_languages.json") if i not in null_values]
    for path in tqdm(glob.glob("data/collected/*.json")):
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


def getLanguageConfidenceStats(glob_path="data/collected/*.json"):
    "count the number of titles for each possible language confidence score"
    dict_counter = {"total":0,"1":0,"0":0,"-1":0,"-2":0}
    for path in tqdm(glob.glob(glob_path)):
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key, value in data.items():
            dict_counter[str(value["language_confidence"])] += 1
            dict_counter["total"] += 1
    print(f"# RESULTS FOR {glob_path}")
    print(f"accuracy of the system : {dict_counter['1']/(dict_counter['total']-dict_counter['0']-dict_counter['-2'])}") # not taking into account null and invalid values
    print(dict_counter)


def dropByLanguageConfidence(treshold=-1.5):
    "drops titles whose language_confidence is inferior to treshold"
    counter = 0
    for path in tqdm(glob.glob("data/collected/*.json")):
        new_data = {}
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if value["language_confidence"] > treshold:
                new_data[key] = value
            else:
                counter += 1
        writeJson(path,new_data)
    print(f"{counter} titles dropped with language_confidence filter")


def dropByLanguageFreq(treshold=10000):
    "drops titles whose language has less titles than the desired treshold" 
    dict_languages = openJson("logs/dict_languages.json")
    counter = 0
    for path in tqdm(glob.glob("data/collected/*.json")):
        new_data = {}
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if dict_languages[value["language"]]["total"] >= treshold:
                new_data[key] = value
            else:
                counter += 1
        writeJson(path,new_data)
    print(f"{counter} titles dropped with language frequency filter")


def createLanguagesFolders():
    "create a specific folder for each language we study"
    removeFolder("data/languages")
    dict_languages = openJson("logs/dict_languages.json")
    createFolder("data/languages")
    for key, value in dict_languages.items():
        createFolder(f"data/languages/{key}")


def sortByLanguage():
    "sort our titles by language in dedicated folders"
    for path in tqdm(glob.glob("data/collected/*.json")):
        dict_lang = {}
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        for key,value in data.items():
            if value["language"] not in dict_lang:
                dict_lang[value["language"]] = {}
            dict_lang[value["language"]][key] = value
        for lang,entries in dict_lang.items():
            writeJson(path.replace("collected",f"languages/{lang}"),entries)


def mergeLanguagesFiles():
    "merge files in each language folder to make consistent json files"
    dict_languages = openJson("logs/dict_languages.json")
    for lang, metadata in dict_languages.items():
        dict_lang = {}
        counter = 0
        file_number = 0
        for path in glob.glob(f"data/languages/{lang}/*json"):
            with open(path,'r',encoding='utf-8') as f:
                data = json.load(f)
            for key,value in data.items():
                dict_lang[key] = value
                counter += 1
                if counter == 200000:
                    writeJson(f"data/languages/{lang}/{lang}_{file_number}.json",dict_lang)
                    file_number += 1
                    counter = 0
                    dict_lang = {}
            os.remove(path) 
        writeJson(f"data/languages/{lang}/{lang}_{file_number}.json",dict_lang)


def languageStep():
    "execute analysis and filters based on languages"
    print("getting languages metadata...")
    getFreqLang()
    checkLang()
    print("attributing language and language confidence score to each title...")
    applyLanguageTag()
    print("dropping titles with low language confidence score...")
    dropByLanguageConfidence()
    print("recounting occurrences of titles for each languages...")
    getFreqLang()
    print("dropping titles from languages with low frequencies...")
    dropByLanguageFreq()
    checkLang()
    print("sorting titles by languages in data/languages...")
    createLanguagesFolders()
    sortByLanguage()
    print("merging json files for each languages...")
    mergeLanguagesFiles()
    print("done !")