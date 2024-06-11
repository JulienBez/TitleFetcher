
import os
import json
import requests

def metadata(year,counter,cursor):
    """vérifie si on a déjà scrappé une partie de la data pour pas la re-scrapper"""
    if not os.path.exists(f'logs/metadata_{year}.json'):
        with open(f'logs/metadata_{year}.json', 'w',encoding="utf'8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
    with open(f'logs/metadata_{year}.json','r',encoding="utf-8") as f:
        metadata = json.load(f)
    if str(counter) not in metadata:
        metadata[counter] = cursor
        with open(f'logs/metadata_{year}.json', 'w',encoding="utf'8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        return False
    return True


def createFolder(folder):
    """crée un dossier"""
    if not os.path.exists(folder): 
        os.makedirs(folder) 


def handleData(results,year,counter):
    """récupère en entrée la data d'une requête et la sauvegarde"""
    dict_papers = {}
    for res in results:
        if res["id"] not in dict_papers:
            dict_papers[res["id"]] = {}
        if res["language"] not in dict_papers[res["id"]]:
            dict_papers[res["id"]][res["language"]] = res["title"]
    with open(f'data/results/{year}/{counter}.json', 'w',encoding="utf'8") as f:
        json.dump(dict_papers, f, indent=4, ensure_ascii=False)  


def mergeJson(files,merge):
    """comme on a beaucoup de data, on fait des merges pour sauver de la place"""
    dict_merge = {}
    for file in files:
        with open(f"data/results/{year}/{file}",'r',encoding="utf-8") as f:
            data = json.load(f)
        dict_merge = {**dict_merge,**data}
    with open(f'data/merge/{year}/{merge}.json', 'w',encoding="utf'8") as f:
        json.dump(dict_merge, f, indent=4, ensure_ascii=False)
    for file in files:
        os.remove(f"data/results/{year}/{file}")

years = ["2020","2021","2022","2023"] # années qu'on veut scrapper
mail = "mailto=julien.bezancon@sorbonne-universite.fr" # mail, nécessaire pour scrapper mieux

createFolder("data")
createFolder("logs")
createFolder("data/results") 
createFolder("data/merge")

for year in years:

    createFolder(f"data/results/{year}")
    createFolder(f"data/merge/{year}")

    cursor = "per-page=200&cursor=*" # curseur pour se déplacer dans les résultats de l'API
    if os.path.exists(f'logs/metadata_{year}.json'): #on cherche le curseur précédent si on reprend une requête ancienne
        with open(f'logs/metadata_{year}.json','r',encoding="utf-8") as f:
            metadataCheck = json.load(f)
        key, cursor = sorted([[int(k),v] for k,v in metadataCheck.items()],reverse=True)[0]
        del metadataCheck[str(key)]
        with open(f'logs/metadata_{year}.json', 'w',encoding="utf'8") as f:
            json.dump(metadataCheck, f, indent=4, ensure_ascii=False)

    filters = f"filter=open_access.is_oa:true,type:types/article,publication_year:{year}" # nos filtres de recherche
    state = 0 # 0 = ça tourne et 1 = on arrête, détermine quand on a finis de scrapper la data pour une année

    merge = 0 # pour nommer nos fichiers merge/
    mergeCheck = os.listdir(f"data/merge/{year}")
    if len(mergeCheck) > 0:
        merge = sorted([int(i.split("/")[-1].replace(".json","")) for i in mergeCheck],reverse=True)[0] + 1
        
    counter = 0 # pour nommer nos fichiers results/

    while state == 0:
        if metadata(year,counter,cursor) == False: #si on a pas de metadata pour l'instance de l'API qu'on parcoure, on la parcoure et on crée une metadata

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
                mergeJson(filesEnd,merge)

            else:
                cursor = f"per-page=200&cursor={data['meta']['next_cursor']}"

        else:
            counter += 1 

        files = os.listdir(f"data/results/{year}")
        if len(files) == 1000:
            mergeJson(files,merge)
            merge += 1