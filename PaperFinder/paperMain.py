# https://openalex.org/works?page=1&filter=open_access.is_oa%3Atrue,type%3Atypes%2Farticle,publication_year%3A2020-2023
# download the result of this query and run this script on it

import os
import json
import pandas as pd

def getDictPapers():
    data = pd.read_csv("data/works-2024-06-10T14-21-23.csv",sep=",")
    dict_papers = {}
    for i,titleId in enumerate(data["id"]):
        if titleId not in dict_papers:
            dict_papers[titleId] = {}
        if data["language"][i] not in dict_papers[titleId]:
            dict_papers[titleId][data["language"][i]] = data["title"][i]
    with open('data/dict_papers.json', 'w',encoding="utf'8") as f:
        json.dump(dict_papers, f, indent=4, ensure_ascii=False)
    

def getLanguagesNumber(dict_papers):
    languages = set()
    for titleId, language in dict_papers.items():
        for k in language.keys():
            languages.add(k)
    return len(languages)


if __name__ == "__main__":

    if not os.path.exists("data/dict_papers.json"):
        print("getting titles... (this might takes a while !)")
        getDictPapers()
        print("titles saved in data/dict_papers.json !")

    print("getting some basic metadata...")
    with open("data/dict_papers.json",'r',encoding="utf-8") as f:
        dict_papers = json.load(f)
    print(f"number of titles : {len(dict_papers.keys())}")
    print(f"number of languages : {getLanguagesNumber(dict_papers)}")
    print("done !")
