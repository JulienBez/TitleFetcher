
import os
import json
import glob
import requests

def saveState(year,counter,cursor):
    "make progressive saves of the current page we are fetching"
    if not os.path.exists(f'logs/saveState_{year}.json'):
        with open(f'logs/saveState_{year}.json', 'w',encoding="utf'8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
    with open(f'logs/saveState_{year}.json','r',encoding="utf-8") as f:
        metadata = json.load(f)
    if str(counter) not in metadata:
        metadata[counter] = cursor
        with open(f'logs/saveState_{year}.json', 'w',encoding="utf'8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        return False
    return True


def createFolder(folder):
    "create a folder"
    if not os.path.exists(folder): 
        os.makedirs(folder) 


def handleData(results,year,counter):
    "for each entry fetched, add it to a dict"
    dict_papers = {}
    for res in results:
        id_clean = res["id"].replace("https://openalex.org/","")
        if id_clean not in dict_papers:
            dict_papers[id_clean] = {"title":res["title"],"language":res["language"],"origin":"paper"}
    with open(f'data/results/{year}/{counter}.json', 'w',encoding="utf'8") as f:
        json.dump(dict_papers, f, indent=4, ensure_ascii=False)  


def mergeJson(files,merge,year):
    "we create a dict for every page (aka. 200 entries/dict). Once every 1000 dict, we merge them and delete them afterwards"
    dict_merge = {}
    for file in files:
        with open(f"data/results/{year}/{file}",'r',encoding="utf-8") as f:
            data = json.load(f)
        dict_merge = {**dict_merge,**data}
    with open(f'data/merge/{year}/papers_{year}_{merge}.json', 'w',encoding="utf'8") as f:
        json.dump(dict_merge, f, indent=4, ensure_ascii=False)
    for file in files:
        os.remove(f"data/results/{year}/{file}")


def changeCursor(year):
    "allows us to resume our collect by fetching the page we were on last time"
    cursor = "per-page=200&cursor=*"
    if os.path.exists(f'logs/saveState_{year}.json'): 
        with open(f'logs/saveState_{year}.json','r',encoding="utf-8") as f:
            metadataCheck = json.load(f)
        key, cursor = sorted([[int(k),v] for k,v in metadataCheck.items()],reverse=True)[0]
        del metadataCheck[str(key)]
        with open(f'logs/saveState_{year}.json', 'w',encoding="utf'8") as f:
            json.dump(metadataCheck, f, indent=4, ensure_ascii=False)
    return cursor


def mergeCheck(year):
    "check the number of merge files to ensure we don't overwrite on top of them"
    merge = 0 
    mergeCheck = os.listdir(f"data/merge/{year}")
    if len(mergeCheck) > 0:
        merge = sorted([int(i.split("/")[-1].replace(".json","")) for i in mergeCheck],reverse=True)[0] + 1
    return merge

    
def getLanguagesNumber(dict_movies):
    "allows us to count the number of languages for one file"
    languages = set()
    counter_null = 0
    for key,value in dict_movies.items():
        if value["language"] == "null":
            counter_null += 1
        else:
            languages.add(value["language"].lower())
    return languages, counter_null 


def getMetadata():
    "check all json files one by one to collect metadatas"
    total_lang = set()
    size = 0
    total_null = 0
    for path in glob.glob("data/merge/*/*.json"):
        with open(path,'r',encoding="utf-8") as f:
            dict_papers = json.load(f)
        lang, counter_null = getLanguagesNumber(dict_papers)
        total_lang.update(lang)
        total_null += counter_null
        size += len(dict_papers.keys())
    return len(total_lang), size, total_null


def collectFromAPI(year,mail):
    "collecter titles from OpenAlex API for a given year"

    createFolder(f"data/results/{year}")
    createFolder(f"data/merge/{year}")

    filters = f"filter=open_access.is_oa:true,type:types/article,publication_year:{year}" # our filters
    state = 0 # 0 = running and 1 = stop

    cursor = changeCursor(year) # cursor pointing to the page we are on
    merge = mergeCheck(year)

    counter = 0 # to name our dict (json) files

    while state == 0:
        if saveState(year,counter,cursor) == False: # if we didn't already scrapped this page

            response = requests.get(f"https://api.openalex.org/works?page=1&{filters}&{mail}&{cursor}") 
            if int(response.status_code) != 200:
                print(response.status_code)
                break

            data = response.json()
            handleData(data["results"],year,counter)
            counter += 1

            if data["meta"]["next_cursor"] is None:
                state = 1
                filesEnd = os.listdir(f"data/results/{year}")
                mergeJson(filesEnd,merge,year)

            else:
                cursor = f"per-page=200&cursor={data['meta']['next_cursor']}" 

        else:
            counter += 1 

        files = os.listdir(f"data/results/{year}")
        if len(files) == 1000:
            mergeJson(files,merge,year)
            merge += 1


if __name__ == "__main__":

    years = ["2020","2021","2022","2023"] # years we want to fetch
    mail = "mailto=<YOURMAIL>" # mail, advised to use it

    createFolder("data")
    createFolder("logs")
    createFolder("data/results") 
    createFolder("data/merge")

    for year in years:
        if not os.path.isdir(f"data/merge/{year}") or len(os.listdir(f"data/merge/{year}")) == 0:
            print(f"getting titles for year {year}... (this might takes a while !)")
            collectFromAPI(year,mail)
            print(f"titles saved in data/merge/{year} !")

    print("getting some basic metadata...")
    nb_lang, size, counter_null = getMetadata()
    print(f"number of titles : {size}")
    print(f"number of languages : {nb_lang}")
    print(f"number of unreferenced language values : {counter_null}")
    print("done !")
