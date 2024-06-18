from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
import pandas as pd

from sklearn.cluster import MiniBatchKMeans
from sklearn.pipeline import make_pipeline

from sentence_transformers import SentenceTransformer, util

from .navigation import *

import time

def vectorizer(titles):
    "vectorize in unigrams and bigrams the seed and the tweet"
    vectorizer = CountVectorizer(ngram_range=(1,2),stop_words=None,lowercase=False)
    return vectorizer.fit_transform(titles)

def test1():
    titles = set()
    #for path in glob.glob("data/languages/fr/*.json"):
    for path in glob.glob("data/frtest/*.json"):
        data = openJson(path)
        for k,v in data.items():
            titles.append(v["title"])
    titles = list(titles)

    start = time.time()

    X = vectorizer(titles)
    X_sparse = csr_matrix(X)

    # Step 2: Clustering with MiniBatchKMeans
    n_clusters = 1000  # Example number of clusters
    batch_size = 10000
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, batch_size=batch_size)
    kmeans.fit(X)

    # Access cluster labels
    cluster_labels = kmeans.labels_

    cluster_dict = {}
    for idx, title in enumerate(titles):
        cluster_label = cluster_labels[idx]
        if cluster_label not in cluster_dict:
            cluster_dict[str(cluster_label)] = []
        cluster_dict[str(cluster_label)].append(title)
    writeJson("temp/clusters.json",cluster_dict)

    end = time.time()
    print(f"executed in {round(end - start,2)}")


#https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/fast_clustering.py
def test2():

    titles = set()
    #for path in glob.glob("data/languages/fr/*.json"):
    for path in glob.glob("data/frtest/*.json"):
        data = openJson(path)
        for k,v in data.items():
            titles.add(v["title"])
    titles = list(titles)

    start = time.time()

    model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    corpus_embeddings = model.encode(titles, batch_size=64, show_progress_bar=True, convert_to_tensor=True)

    end = time.time()
    print(f"embeddings executed in {round(end - start,2)}")

    start_time = time.time()

    # Two parameters to tune:
    # min_cluster_size: Only consider cluster that have at least 25 elements
    # threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
    clusters = util.community_detection(corpus_embeddings, min_community_size=25, threshold=0.75)

    end = time.time()
    print(f"clustering executed in {round(end - start,2)}")

    for i, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(i + 1, len(cluster)))
        for sentence_id in cluster[0:3]:
            print("\t", titles[sentence_id])
        print("\t", "...")
        for sentence_id in cluster[-3:]:
            print("\t", titles[sentence_id])