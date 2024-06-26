import numpy as np

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

from .navigation import *

def extractTitlesFromLanguage(language):
    ""
    titles = {}
    for path in glob.glob(f"data/languages/{language}/*.json"):
        data = openJson(path)
        for k,v in data.items():
            if v["title"] not in titles:
                titles[v["title"]] = []
            titles[v["title"]].append(k)
        writeJson(f"logs/languages/dict_{language}.json",titles)
    return np.array([i for i in list(titles.keys()) if i is not None])


def extractTitlesFromClusters(global_path):
    ""
    titles = []
    for path in glob.glob(global_path):
        data = openJson(path)
        for k,v in data.items():
            titles = titles + v
    return np.array(titles)
    

def KMeansClustering(titles,vectorizer,language,iteration=0):
    ""

    removeFolder(f"data/clusters/{language}/{iteration}")
    createFolder(f"data/clusters/{language}/{iteration}")

    X = vectorizer.fit_transform(titles)
    
    kmean = KMeans(n_clusters=15,n_init=10)
    kmean.fit(X)
    clusters = kmean.labels_

    for cluster in list(set(clusters)):
        res = {}
        titles_clusters = titles[clusters == cluster]
        res[str(cluster)] = list(titles_clusters)
        writeJson(f"data/clusters/{language}/{iteration}/{language}_{str(cluster)}.json",res)


def DBscanClustering(titles,vectorizer):
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


def clusterViewer(clusters):
    ""

    import matplotlib.pyplot as plt
    from sklearn.decomposition import TruncatedSVD #marche avec la sparse matrix direct
    import itertools

    all_titles = list(itertools.chain(*clusters.values()))

    vectorizer = CountVectorizer(ngram_range=(1, 1), stop_words=None, lowercase=True)
    X = vectorizer.fit_transform(all_titles)

    svd = TruncatedSVD(n_components=2)
    X_reduced = svd.fit_transform(X)  # Works directly with the sparse matrix   

    colors = plt.cm.rainbow(np.linspace(0, 1, len(clusters)))

    clusters_2d_points = {}

    index = 0 
    for cluster_id, titles in clusters.items():
        clusters_2d_points[cluster_id] = X_reduced[index:index + len(titles)]
        index += len(titles)

    fig, ax = plt.subplots(figsize=(12, 10))

    for cluster_id, points in clusters_2d_points.items():
        ax.scatter(points[:, 0], points[:, 1], label=f'Cluster {cluster_id}', s=50, alpha=0.75)

    #ax.set_xlabel('Component 1')
    #ax.set_ylabel('Component 2')
    #ax.set_title('2D Visualization of Clusters')
    ax.legend()

    plt.show()