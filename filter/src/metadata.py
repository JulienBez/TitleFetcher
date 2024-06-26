from itertools import chain
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
import numpy as np
import math

from .navigation import *

def getBasicMetadatas():
    "get some basic metadatas for each language"

    dict_metadata = {}
    dict_languages = openJson("logs/dict_languages.json")

    for lang, occurrences in tqdm(dict_languages.items()):

        dict_lang = {"totalTitles":0,"totalToken":0,"totalChar":0,"bigramSize":set(),"trigramSize":set(),"vocabularySize":set(),"meanToken":0,"meanChar":0,"byOrigin":{}}

        for path in glob.glob(f"data/languages/{lang}/*json"):

            data = openJson(path)

            for key, value in data.items():

                title = value["title"]
                titleSplit = title.split()
                titleOrigin = value["origin"]

                if titleOrigin not in dict_lang["byOrigin"]:
                    dict_lang["byOrigin"][titleOrigin] = {"totalTitles":0,"totalToken":0,"totalChar":0,"bigramSize":set(),"trigramSize":set(),"vocabularySize":set()}

                dict_lang["byOrigin"][titleOrigin]["totalTitles"] += 1
                dict_lang["byOrigin"][titleOrigin]["totalChar"] += len(title)
                dict_lang["byOrigin"][titleOrigin]["totalToken"] += len(titleSplit)

                for word in titleSplit:
                    dict_lang["byOrigin"][titleOrigin]["vocabularySize"].add(word)

                bigrams = [title[i:i+2] for i in range(len(title)-1)]
                for bi in bigrams:
                    dict_lang["byOrigin"][titleOrigin]["bigramSize"].add(bi)

                trigrams = [title[i:i+3] for i in range(len(title)-1)]
                for tri in trigrams:
                    dict_lang["byOrigin"][titleOrigin]["trigramSize"].add(tri)

        for origin, numbers in dict_lang["byOrigin"].items():

            dict_lang["totalTitles"] += numbers["totalTitles"]
            dict_lang["totalChar"] += numbers["totalChar"]
            dict_lang["totalToken"] += numbers["totalToken"]
            dict_lang["vocabularySize"] = dict_lang["vocabularySize"].union(numbers["vocabularySize"])
            dict_lang["bigramSize"] = dict_lang["bigramSize"].union(numbers["bigramSize"])
            dict_lang["trigramSize"] = dict_lang["trigramSize"].union(numbers["trigramSize"])

            dict_lang["byOrigin"][origin]["meanChar"] = numbers["totalChar"]/numbers["totalTitles"]
            dict_lang["byOrigin"][origin]["meanToken"] = numbers["totalToken"]/numbers["totalTitles"]
            dict_lang["byOrigin"][origin]["vocabularySize"] = len(numbers["vocabularySize"])
            dict_lang["byOrigin"][origin]["bigramSize"] = len(numbers["bigramSize"])
            dict_lang["byOrigin"][origin]["trigramSize"] = len(numbers["trigramSize"])
                   
        dict_lang["meanChar"] = dict_lang["totalChar"]/occurrences
        dict_lang["meanToken"] = dict_lang["totalToken"]/occurrences
        dict_lang["vocabularySize"] = len(dict_lang["vocabularySize"])
        dict_lang["bigramSize"] = len(dict_lang["bigramSize"])
        dict_lang["trigramSize"] = len(dict_lang["trigramSize"])

        dict_metadata[lang] = dict_lang    

    writeJson("logs/dict_metadata.json",dict_metadata)


def getBasicMetadatasHistogram(logscale=True):
    "take our dict of metadata as input and create a histogram to visualize it"

    dict_metadata = openJson("logs/dict_metadata.json")

    order_lang = []
    total_paper = []
    total_movie = []
    total_press = []

    for lang, values in dict_metadata.items():
        
        order_lang.append(lang)

        if "paper" in values["byOrigin"]:
            total_paper.append(values["byOrigin"]["paper"]["totalTitles"])
        else:
            total_paper.append(0)

        if "movie" in values["byOrigin"]:
            total_movie.append(values["byOrigin"]["movie"]["totalTitles"])
        else:
            total_movie.append(0)

        if "press" in values["byOrigin"]:
            total_press.append(values["byOrigin"]["press"]["totalTitles"])
        else:
            total_press.append(0)

    width = 0.5
    fig, ax = plt.subplots()
    ax.bar(order_lang,total_paper,label="paper",width=width,color='red')
    ax.bar(order_lang,total_press,bottom=total_paper,label="press",width=width,color='green')

    bottom_movie = np.array(total_paper) + np.array(total_press)
    ax.bar(order_lang, total_movie, bottom=bottom_movie, label="movie", width=width, color='blue')

    path = 'logs/images/dict_metadata.png'
    if logscale:
        ax.set_yscale('log')
        path = 'logs/images/dict_metadata_logscale.png'

    ax.legend()
    plt.xticks(rotation=50, ha='right')
    plt.tight_layout()
    plt.savefig(path,dpi=1000)


def getDataVizualisation(vectorizer,studiedOrigins=["movie","paper","press"],number=10):
    "for each language, plot its titles vectors points to see if clustering might helps us"
    "vectorizer : a vectorized list of titles"
    "studiedOrigins : the origins we want to study via vizualisation"
    "number : the max number of languages we want to analyze, take the <number> most populated languages"

    name = "_".join(studiedOrigins)

    createFolder("logs/images")
    createFolder("logs/images/getDataVizualisation")
    createFolder(f"logs/images/getDataVizualisation/{name}")

    dict_languages = openJson("logs/dict_languages.json")
    sorted_dict_languages = [i[0] for i in sorted(dict_languages.items(), key=lambda x:x[1],reverse=True)]

    #we want to adjust our graph size according to number
    if number > len(sorted_dict_languages):
        number = len(sorted_dict_languages)

    #determine the number of lines and columns from number
    nlines = 3
    ncols = math.ceil(number/nlines)#round up to next integer
    if number < nlines:
        nlines = number
        ncols = 1
    
    #create a fig with multiple subplots according to number of line and columns
    fig, axs = plt.subplots(ncols, nlines, figsize=(15, 15), sharex=True, sharey=True) #to have number of col and lines
    fig.tight_layout()

    for lang, ax in tqdm(zip(sorted_dict_languages[0:number],axs.ravel()), total=number):

        titles = []
        origins = []
        for path in glob.glob(f"data/languages/{lang}/*.json"):
            data = openJson(path)
            for k,v in data.items():
                if v["origin"] in studiedOrigins:
                    titles.append(v["title"])
                    origins.append(v["origin"])

        if len(titles) > 0:

            X = vectorizer.fit_transform(titles)

            svd = TruncatedSVD(n_components=2)
            X_reduced = svd.fit_transform(X)  # Works directly with the sparse matrix   

            colors = []
            for origin in origins:
                if origin == "press":
                    colors.append("green")
                elif origin == "movie":
                    colors.append("blue")
                elif origin == "paper":
                    colors.append("red")

            colsNames = []
            labsNames = []
            for so in studiedOrigins:
                if so == "press":
                    colsNames.append("green")
                    labsNames.append(so)
                if so == "movie":
                    colsNames.append("blue")
                    labsNames.append(so)
                if so == "paper":
                    colsNames.append("red")
                    labsNames.append(so)

            ax.scatter(X_reduced[:, 0], X_reduced[:, 1], c=colors, alpha=0.2, s=10)

            handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markerfacecolor=color, markersize=10) for color, label in zip(colsNames,labsNames)]
            ax.legend(handles=handles, title='Categories')

            #plt.xlabel('SVD Component 1')
            #plt.ylabel('SVD Component 2')
            ax.set_title(f'{lang}')
            ax.grid(True) 

        else:
            print(f"{lang} has no titles from the following sources : {','.join(studiedOrigins)}")

    vectorizeName = "".join(x for x in str(vectorizer).replace(" ","_") if x.isalnum() or x == "_")
    plt.savefig(f"logs/images/getDataVizualisation/{name}/{number}_{vectorizeName}.png")
        

    