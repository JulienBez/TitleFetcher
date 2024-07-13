import numpy as np

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

from .navigation import *

def KMeansClustering(vectorizer,genres,number,n_clusters=10):
    ""

    vectorizeName = "".join(x for x in str(vectorizer).replace(" ","_") if x.isalnum() or x == "_")
    createFolder(f"data/clusters")

    dict_languages = openJson("logs/dict_languages.json")
    sorted_dict_languages = [i[0] for i in sorted(dict_languages.items(), key=lambda x:x[1],reverse=True)]

    for lang in tqdm(sorted_dict_languages[0:number]):

        createFolder(f"data/clusters/{lang}")
        createFolder(f"data/clusters/{lang}/{('_').join(genres)}")

        titles, origins = getTitles(lang,genres)

        if len(titles) > n_clusters:

            X = getVectors(vectorizer,titles,lang,genres)
            
            kmean = KMeans(n_clusters=n_clusters,n_init=10)
            kmean.fit(X)

            res = {int(cluster):[] for cluster in sorted(kmean.labels_)}
            for cluster, title in zip(kmean.labels_, titles):
                res[int(cluster)].append(title)
            writeJson(f"data/clusters/{lang}/{('_').join(genres)}/KMeans_{vectorizeName}.json",res)


def DBscanClustering(vectorizer,genres):
    ""

    vectorizeName = "".join(x for x in str(vectorizer).replace(" ","_") if x.isalnum() or x == "_")
    createFolder(f"data/clusters")

    dict_languages = openJson("logs/dict_languages.json")
    sorted_dict_languages = [i[0] for i in sorted(dict_languages.items(), key=lambda x:x[1],reverse=True)]

    l = ["fr"]
    for lang in l:
    #for lang in tqdm(sorted_dict_languages[0:number]):

        if os.path.exists(f"data/clusters/{lang}/{('_').join(genres)}/KMeans_{vectorizeName}.json"):

            titles, origins = getTitles(lang,genres)
            X = getVectors(vectorizer,titles,lang,genres)
            
            dbscan = DBSCAN(eps=0.9, min_samples=2)
            dbscan.fit_predict(X)

            clusters = {}
            for title, label in zip(titles, dbscan.labels_):
                if str(label) not in clusters:
                    clusters[str(label)] = []
                clusters[str(label)].append(title)
            writeJson(f"data/clusters/{lang}/{('_').join(genres)}/DBscan_{vectorizeName}.json",clusters) 


def OLDDBscanClustering(titles,vectorizer):
    ""
        
    X = vectorizer.fit_transform(titles)

    #cosine_sim_matrix = cosine_similarity(X,dense_output=False)

    dbscan = DBSCAN(eps=0.9, min_samples=2)
    #dbscan = DBSCAN(eps=0.2, min_samples=2, metric='precomputed')

    labels = dbscan.fit_predict(X)

    clusters = {}
    for title, label in zip(titles, labels):
        if str(label) not in clusters:
            clusters[str(label)] = []
        clusters[str(label)].append(title)
    writeJson("test.json",clusters)


def clusterAnalyzer():
    ""

    #dict_languages = openJson("logs/dict_languages.json")
    dict_languages = {"fr":1}

    createFolder("data/clusters")
    createFolder("logs/languages")

    vectorizer = TfidfVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")

    for language, occurrence in dict_languages.items():

        createFolder(f"data/clusters/{language}")
        createFolder(f"logs/languages/{language}")

        #titles = extractTitlesFromLanguage(language)
        #titles = extractTitlesFromClusters(f"data/clusters/{language}/0/*_9.json")
        #KMeansClustering(titles,language,iteration=1)

        """
        clusters = {}
        for path in glob.glob(f"data/clusters/{language}/1/*.json"): #modif lang variable
            data = openJson(path)
            for k,v in data.items():
                clusters[k] = v
        clusterViewer(clusters)

        clusters = {"all":[]}
        for path in glob.glob(f"data/languages/{language}/*.json"): #modif lang variable
            data = openJson(path)
            for k,v in data.items():
                if v["origin"] == "press" and v["title"] is not None:
                    clusters["all"].append(v["title"])
        clusterViewer(clusters)

        clusters = {}
        for path in glob.glob(f"data/languages/{language}/*.json"): #modif lang variable
            data = openJson(path)
            for k,v in data.items():
                if v["origin"] not in clusters:
                    clusters[v["origin"]] = []
                if v["title"] is not None:
                    clusters[v["origin"]].append(v["title"])
        clusterViewer(clusters)
        """

        #test_dbscan = openJson(f"data/clusters/{language}/0/{language}_9.json")
        #DBscanClustering(test_dbscan)

