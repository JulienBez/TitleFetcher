import os
import numpy as np

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

from scipy.sparse import csr_matrix

from .navigation import *

import time

def KMeansClustering(language,iteration=0):
    ""

    titles = {}

    for path in glob.glob(f"data/languages/{language}/*.json"): #modif lang variable
        data = openJson(path)
        for k,v in data.items():
            if v["title"] not in titles:
                titles[v["title"]] = []
            titles[v["title"]].append(k)
        writeJson(f"logs/languages/dict_{language}.json",titles)

    titles_only = np.array([i for i in list(titles.keys()) if i is not None])
    del titles

    vectorizer = CountVectorizer(ngram_range=(1,1),stop_words=None,lowercase=True)
    X = vectorizer.fit_transform(titles_only)
    
    kmean = KMeans(n_clusters=15,n_init=10)
    kmean.fit(X)
    clusters = kmean.labels_

    createFolder(f"data/clusters/{language}/{iteration}")

    for cluster in list(set(clusters)):
        res = {}
        titles_clusters = titles_only[clusters == cluster]
        res[str(cluster)] = list(titles_clusters)
        writeJson(f"data/clusters/{language}/{iteration}/{language}_{str(cluster)}.json",res)


def DBscanClustering(cluster):
    ""

    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA

    for key, value in cluster.items():
        titles = value

        vectorizer = CountVectorizer(ngram_range=(1,1),stop_words=None,lowercase=True)
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

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X.toarray())
        
        fig, ax = plt.subplots(figsize=(10, 8))

        ax.scatter(X_pca[:, 0], X_pca[:, 1], c='blue', marker='o')
        # Scatter plot for t-SNE (if you used t-SNE instead of PCA, uncomment the following line)
        # ax.scatter(X_tsne[:, 0], X_tsne[:, 1], c='red', marker='x')

        # Set labels and title
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_title('2D Visualization of Title Vectors')

        # Show the plot
        plt.show()



def clusterAnalyzer():
    ""

    #dict_languages = openJson("logs/dict_languages.json")

    dict_languages = {"fr":1}

    createFolder("data/clusters")
    createFolder("logs/languages")

    for language, occurrence in dict_languages.items():

        #removeFolder(f"data/clusters/{language}")
        #removeFolder(f"logs/languages/{language}")

        #createFolder(f"data/clusters/{language}")
        #createFolder(f"logs/languages/{language}")

        #KMeansClustering(language)

        clusters = {}
        for path in glob.glob(f"data/clusters/{language}/0/*.json"): #modif lang variable
            data = openJson(path)
            for k,v in data.items():
                clusters[k] = len(v)
        print(clusters)

        test_dbscan = openJson(f"data/clusters/{language}/0/{language}_9.json")
        DBscanClustering(test_dbscan)


def sentenceTransformersClustering(global_path="data/samples"):
    #https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/fast_clustering.py
    
    from sentence_transformers import SentenceTransformer, util

    languages = os.listdir(global_path)
    model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    createFolder("data/clusters")

    for language in languages:

        print(f"\n~#~# {language} #~#~\n")

        titles = {}

        for path in glob.glob(f"{global_path}/{language}/*.json"):
            data = openJson(path)
            for k,v in data.items():
                if v["title"] not in titles:
                    titles[v["title"]] = []
                titles[v["title"]].append(k)
        titles_only = list(titles.keys())

        print("starting embeddings...")
        start = time.time()

        corpus_embeddings = model.encode(titles_only, batch_size=64, show_progress_bar=True, convert_to_tensor=True)

        end = time.time()
        print(f"embeddings executed in {round(end - start,2)} !")

        print("starting clustering...")
        start_time = time.time()

        # Two parameters to tune:
        # min_cluster_size: Only consider cluster that have at least 25 elements
        # threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
        clusters = util.community_detection(corpus_embeddings, min_community_size=25, threshold=0.75)

        end = time.time()
        print(f"clustering executed in {round(end - start,2)} !")

        dict_cluster = {}
        for i, cluster in enumerate(clusters):
            if str(i) not in dict_cluster:
                dict_cluster[str(i)] = []
            for sentence_id in cluster:
                title_index = titles_only[sentence_id]
                dict_cluster[str(i)].append({title_index:titles[title_index]})
        writeJson(f"data/clusters/{language}.json",dict_cluster)


#imports

    #instanciations variables

    #début boucle par langue

        #vectorisation sur TOUS LES TITRES

        #début boucle par fichier dans langue (enumerate pour récup les index)

            #récupérer coordonnées des titres dans ce fichier dans l'espace vectoriel

            #similarité cosinus

            #dbscan clusters

            #sauvegarde des clusters pour ce fichier

        #union des clusters de chaque fichier par centroids ? par similarité ?

        #sauvegarde cluster général