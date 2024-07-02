import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from .navigation import *
from .clustering import *

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

    createFolder("logs/images")
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
    plt.savefig(path,dpi=1000,bbox_inches='tight')
    plt.close()


def getVizualisation(vectorizer,genres,number,clusters=False,clusteType="Kmeans"):
    "for each language, plot its titles vectors points to see if clustering might helps us"

    name = "_".join(genres)
    vectorizeName = "".join(x for x in str(vectorizer).replace(" ","_") if x.isalnum() or x == "_")

    createFolder("logs/images")

    folderName = "getDataVizualisation"
    if clusters:
        folderName = "getClustersVizualisation"

    createFolder(f"logs/images/{folderName}")
    createFolder(f"logs/images/{folderName}/{name}")

    if not os.path.isfile(f"logs/images/{folderName}/{name}/{number}_{vectorizeName}.png"):

        # we sort our languages to select the top <number>
        dict_languages = openJson("logs/dict_languages.json")
        sorted_dict_languages = [i[0] for i in sorted(dict_languages.items(), key=lambda x:x[1],reverse=True)]

        # we want to adjust our graph size according to <number>
        if number > len(sorted_dict_languages):
            number = len(sorted_dict_languages)

        # determine the number of lines and columns from <number>
        nlines = 3
        ncols = math.ceil(number/nlines) # round up to next integer
        if number < nlines:
            nlines = number
            ncols = 1
        
        # create a fig with multiple subplots according to number of line and columns
        fig, axs = plt.subplots(ncols, nlines, figsize=(15, 15), sharex=True, sharey=True) # to have number of col and lines
        fig.tight_layout()

        # for each language and subplot in range of indicated number
        for lang, ax in tqdm(zip(sorted_dict_languages[0:number],axs.ravel()), total=number):

            # we collect titles and their origins
            titles, origins = getTitles(lang,genres)
            if clusters:
                origins = getClustersTags(vectorizer,lang,genres,titles,clusteType)

            if len(titles) > 0:

                # we vectorize our titles to plot their vectors
                X = getVectors(vectorizer,titles,lang,genres)
                svd = TruncatedSVD(n_components=2)
                X_reduced = svd.fit_transform(X)  # Works directly with the sparse matrix   

                # we color each genre differently and we get our labels
                rainbow_colors = iter(plt.cm.rainbow(np.linspace(0, 1, len(set(origins)))))
                colors = origins
                colors_labels = []
                origins_labels = []
                for genre, c in zip(set(origins), rainbow_colors):
                    colors_labels.append(c)
                    origins_labels.append(genre)
                    for i, origin in enumerate(colors):
                        if type(origin) == str and origin == genre:
                            colors[i] = c

                # we do the vizualisation
                ax.scatter(X_reduced[:, 0], X_reduced[:, 1], c=colors, alpha=0.2, s=10)
                handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markerfacecolor=color, markersize=10) for color, label in zip(colors_labels,origins_labels)]
                legend_title = "Categories"
                if clusters == True:
                    legend_title = "Clusters"
                ax.legend(handles=handles, title=legend_title)
                ax.set_title(f'{lang}')
                ax.grid(True)

            else:
                print(f"{lang} has no titles from the following sources : {','.join(genres)}")

        plt.savefig(f"logs/images/{folderName}/{name}/{number}_{vectorizeName}.png",bbox_inches='tight')
        plt.close()
        

def dataVisualisationLoop(genres,number):
    "proceed getDataVizualisation with different parameters"
    
    timeWindowsName = f"{number}_{('_').join(genres)}"
    runtimePath = "logs/images/runtimes.json"

    if not os.path.isfile(runtimePath):
        writeJson(runtimePath,[])

    ngrams = [(1,1),(2,2)]
    analyzers = ["char","word","char_wb"]

    stop_words = None
    lowercase = True

    for ngram in ngrams:
        for analyzer in analyzers:

            start = time.time()

            vectorizer = TfidfVectorizer(ngram_range=ngram, stop_words=stop_words, lowercase=lowercase, analyzer=analyzer)
            getVizualisation(vectorizer,genres,number)

            end = time.time()
        
            runtimes = openJson(runtimePath)
            runtimes.append([timeWindowsName,str(vectorizer),round(end - start,2)])
            writeJson(runtimePath,runtimes)


def getGenresPerClusters(vectorizer,genres,number,clusteType):
    ""

    name = "_".join(genres)
    vectorizeName = "".join(x for x in str(vectorizer).replace(" ","_") if x.isalnum() or x == "_")

    createFolder("logs/images")

    folderName = "getGenrePerClusters"

    createFolder(f"logs/images/{folderName}")
    createFolder(f"logs/images/{folderName}/{name}")

    if not os.path.isfile(f"logs/images/{folderName}/{name}/{number}_{vectorizeName}.png"):

        # we sort our languages to select the top <number>
        dict_languages = openJson("logs/dict_languages.json")
        sorted_dict_languages = [i[0] for i in sorted(dict_languages.items(), key=lambda x:x[1],reverse=True)]

        # we want to adjust our graph size according to <number>
        if number > len(sorted_dict_languages):
            number = len(sorted_dict_languages)

        # determine the number of lines and columns from <number>
        nlines = 3
        ncols = math.ceil(number/nlines) # round up to next integer
        if number < nlines:
            nlines = number
            ncols = 1
        
        # create a fig with multiple subplots according to number of line and columns
        fig, axs = plt.subplots(ncols, nlines, figsize=(15, 15), sharex=True, sharey=True) # to have number of col and lines
        fig.tight_layout()

        # for each language and subplot in range of indicated number
        for lang, ax in tqdm(zip(sorted_dict_languages[0:number],axs.ravel()), total=number):

            titles, origins = getTitles(lang,genres)
            clusterTags = getClustersTags(vectorizer,lang,genres,titles,clusteType)

            dict_res = {}
            for i,tag in enumerate(clusterTags):
                if tag not in dict_res:
                    dict_res[tag] = {"movie":0,"paper":0,"press":0}
                dict_res[tag][origins[i]] += 1
            dict_res = sorted([{"tag":k,**v} for k,v in dict_res.items()], key=lambda k: k['tag'])

            tag_order = [i["tag"] for i in dict_res]
            total_movie = [i["movie"] for i in dict_res]
            total_paper = [i["paper"] for i in dict_res]
            total_press = [i["press"] for i in dict_res]

            width = 0.5

            ax.bar(tag_order,total_paper,label="paper",width=width,color='red')
            ax.bar(tag_order,total_press,bottom=total_paper,label="press",width=width,color='green')

            bottom_movie = np.array(total_paper) + np.array(total_press)
            ax.bar(tag_order, total_movie, bottom=bottom_movie, label="movie", width=width, color='blue')

            ax.set_title(f'{lang}')
            ax.legend()

        plt.savefig(f"logs/images/{folderName}/{name}/{number}_{vectorizeName}.png",dpi=1000,bbox_inches='tight')
        plt.close()
