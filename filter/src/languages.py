from .navigation import *

def sortByLanguage():
    "sort each title according to its language in a dedicated folder and remove titles with 'null' as value"
    dict_languages = {}
    number_null = 0
    removeFolder("data/languages")
    createFolder("data/languages")
    for path in tqdm(glob.glob("data/collected/*.json")):
        data = openJson(path)
        dict_lang = {}
        for key,value in data.items():
            if value["title"] == "null" or value["title"] is None:
                number_null += 1
            else: 
                lang = value["language"]
                if lang not in dict_languages:
                    dict_languages[lang] = 0
                    createFolder(f"data/languages/{lang}")
                dict_languages[lang] += 1
                if lang not in dict_lang:
                    dict_lang[lang] = {}
                dict_lang[lang][key] = value
        for lang,entries in dict_lang.items():
            writeJson(path.replace("collected",f"languages/{lang}"),entries)
    writeJson("logs/dict_languages.json",dict(sorted(dict_languages.items(), key=lambda x:x[1], reverse=True)))
    print(f"dropped {number_null} titles with 'null' as value")
        

def dropNulls(nulls = ["\\N","null"]):
    "drops titles whose language is 'null'"
    dict_languages = openJson("logs/dict_languages.json")
    new_dict_languages = {}
    counter = 0
    for lang, occurrences in tqdm(dict_languages.items()):
        if str(lang) in nulls:
            counter += occurrences
            removeFolder(f"data/languages/{lang}")
        else:
            new_dict_languages[lang] = occurrences
    writeJson("logs/dict_languages.json",new_dict_languages)
    print(f"dropped {counter} titles with 'null' as language")


def dropLows(treshold=10000):
    "drops titles whose language has less titles than the desired treshold"
    dict_languages = openJson("logs/dict_languages.json")
    new_dict_languages = {}
    counter = 0
    for lang, occurrences in tqdm(dict_languages.items()):
        if occurrences < treshold:
            counter += occurrences
            removeFolder(f"data/languages/{lang}")
        else:
            new_dict_languages[lang] = occurrences
    writeJson("logs/dict_languages.json",new_dict_languages)
    print(f"dropped {counter} titles from low frequencies languages")


def mergeLanguagesFiles(size=100000):
    "merge files in each language folder to make consistent json files"
    dict_languages = openJson("logs/dict_languages.json")
    for lang, occurrences in tqdm(dict_languages.items()):
        dict_lang = {}
        counter = 0
        file_number = 0
        for path in glob.glob(f"data/languages/{lang}/*json"):
            data = openJson(path)
            for key,value in data.items():
                dict_lang[key] = value
                counter += 1
                if counter == size:
                    writeJson(f"data/languages/{lang}/{lang}_{file_number}.json",dict_lang)
                    file_number += 1
                    counter = 0
                    dict_lang = {}
            os.remove(path)
        writeJson(f"data/languages/{lang}/{lang}_{file_number}.json",dict_lang)


def languageStep():
    "execute analysis and filters based on languages"
    print("sorting titles by language...")
    sortByLanguage()
    print("droppping titles with 'null' as language...")
    dropNulls()
    print("dropping titles from low frequencies languages...")
    dropLows()
    print("merging files in each language folder...")
    mergeLanguagesFiles()
    print("done !")
    
