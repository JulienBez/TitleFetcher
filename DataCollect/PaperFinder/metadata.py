import os
import json
import glob

if __name__ == "__main__":

    print("getting some basic metadata...")

    languages = set()
    counter = 0
    getTags = 1

    for path in glob.glob("PaperFinder/data/merge/*/*.json"):

        #GET TAGS#
        if getTags == 1:
            with open(path,'r',encoding="utf-8") as f:
                dict_paper = json.load(f)
            for k,v in dict_paper.items():
                v["origin"] = "paper"
            with open(path, 'w',encoding="utf'8") as f:
                json.dump(dict_paper, f, indent=4, ensure_ascii=False)

        # GET METADATA #
        with open(path,'r',encoding="utf-8") as f:
            dict_paper = json.load(f)
        counter += len(dict_paper.keys())
        for key,value in dict_paper.items():
            for k in value.keys():
                languages.add(k)

    print(f"number of titles : {counter}")
    print(f"number of languages : {len(languages)}")
    print("done !")
