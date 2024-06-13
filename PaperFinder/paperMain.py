
import os
import json
import requests

def metadata(year,counter,cursor):
    "make progressive saves of the current page we are fetching"
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
    "create a folder"
    if not os.path.exists(folder): 
        os.makedirs(folder) 


def handleData(results,year,counter):
    "for each entry fetched, add it to a dict"
    dict_papers = {}
    for res in results:
        if res["id"] not in dict_papers:
            dict_papers[res["id"]] = {}
        if res["language"] not in dict_papers[res["id"]]:
            dict_papers[res["id"]][res["language"]] = res["title"]
    with open(f'data/results/{year}/{counter}.json', 'w',encoding="utf'8") as f:
        json.dump(dict_papers, f, indent=4, ensure_ascii=False)  


def mergeJson(files,merge):
    "we create a dict for every page (aka. 200 entries/dict). Once every 1000 dict, we merge them and delete them afterwards"
    dict_merge = {}
    for file in files:
        with open(f"data/results/{year}/{file}",'r',encoding="utf-8") as f:
            data = json.load(f)
        dict_merge = {**dict_merge,**data}
    with open(f'data/merge/{year}/{merge}.json', 'w',encoding="utf'8") as f:
        json.dump(dict_merge, f, indent=4, ensure_ascii=False)
    for file in files:
        os.remove(f"data/results/{year}/{file}")


if __name__ == "__main__":

    years = ["2020","2021","2022","2023"] # years we want to fetch
    mail = "mailto=<YOURMAIL>" # mail, advised to use it

    createFolder("data")
    createFolder("logs")
    createFolder("data/results") 
    createFolder("data/merge")

    for year in years:

        createFolder(f"data/results/{year}")
        createFolder(f"data/merge/{year}")

        # CHANGE CURSOR #
        cursor = "per-page=200&cursor=*" # cursor to navigate from page to page
        if os.path.exists(f'logs/metadata_{year}.json'): 
            with open(f'logs/metadata_{year}.json','r',encoding="utf-8") as f:
                metadataCheck = json.load(f)
            key, cursor = sorted([[int(k),v] for k,v in metadataCheck.items()],reverse=True)[0]
            del metadataCheck[str(key)]
            with open(f'logs/metadata_{year}.json', 'w',encoding="utf'8") as f:
                json.dump(metadataCheck, f, indent=4, ensure_ascii=False)

        filters = f"filter=open_access.is_oa:true,type:types/article,publication_year:{year}" # our filters
        state = 0 # 0 = running and 1 = stop

        merge = 0 # to name our merge files + we check if merge files already exist just in case
        mergeCheck = os.listdir(f"data/merge/{year}")
        if len(mergeCheck) > 0:
            merge = sorted([int(i.split("/")[-1].replace(".json","")) for i in mergeCheck],reverse=True)[0] + 1

        counter = 0 # to name our dict (json) files

        while state == 0:
            if metadata(year,counter,cursor) == False: # if we didn't already scrapped this page

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