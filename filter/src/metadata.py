import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from .navigation import *

def getBasicMetadatas():
    "get some basic metadatas for each language"

    dict_metadata = {}
    dict_languages = openJson("logs/dict_languages.json")

    for lang, occurrences in tqdm(dict_languages.items()):

        dict_lang = {
            "totalTitles":0,"totalToken":0,
            "totalChar":0,"bigramSize":set(),
            "trigramSize":set(),"vocabularySize":set(),
            "meanToken":0,"meanChar":0
            }

        for path in glob.glob(f"data/languages/{lang}/*json"):

            data = openJson(path)

            for key, value in data.items():

                title = value["title"]
                titleSplit = title.split()

                dict_lang["totalTitles"] += 1
                dict_lang["totalChar"] += len(title)
                dict_lang["totalToken"] += len(titleSplit)

                for word in titleSplit:
                    dict_lang["vocabularySize"].add(word)

                bigrams = [title[i:i+2] for i in range(len(title)-1)]
                for bi in bigrams:
                    dict_lang["bigramSize"].add(bi)

                trigrams = [title[i:i+3] for i in range(len(title)-1)]
                for tri in trigrams:
                    dict_lang["trigramSize"].add(tri)
                   
        dict_lang["meanChar"] = dict_lang["totalChar"]/occurrences
        dict_lang["meanToken"] = dict_lang["totalToken"]/occurrences
        dict_lang["vocabularySize"] = len(dict_lang["vocabularySize"])
        dict_lang["bigramSize"] = len(dict_lang["bigramSize"])
        dict_lang["trigramSize"] = len(dict_lang["trigramSize"])

        dict_metadata[lang] = dict_lang    

    writeJson("logs/dict_metadata.json",dict_metadata)


def getBasicMetadatasHistogram(logscale=True):
    "take our dict of metadata as input and create a histogram to visualize it"

    createFolder("logs/images")
    dict_metadata = openJson("logs/dict_metadata.json")

    order_lang = []
    total = []

    for lang, values in dict_metadata.items():    

        order_lang.append(lang)    
        total.append(values["totalTitles"])

    width = 0.5
    fig, ax = plt.subplots()

    ax.bar(order_lang, total, label="titles", width=width, color='blue')

    path = 'logs/images/dict_metadata.png'
    if logscale:
        ax.set_yscale('log')
        path = 'logs/images/dict_metadata_logscale.png'

    ax.legend()
    plt.xticks(rotation=50, ha='right')
    plt.tight_layout()
    plt.savefig(path,dpi=1000,bbox_inches='tight')
    plt.close()
