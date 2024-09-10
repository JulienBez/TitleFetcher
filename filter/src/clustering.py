from .navigation import *

def DBSCAN():
    ""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import DBSCAN
    import json

    # Example list of sentences
    queries = [c["query"] for c in openJson("test.json")]
    sentences = []
    for cluster in openJson("test.json"):
        voc = set()
        for title in cluster["cluster"]:
            ngram = [title.lower()[i:i+3] for i in range(len(title)-1)]
            for n in ngram:
                voc.add(n)
        sentences.append(" ".join(list(voc)))
        queries.append(cluster["query"])

    # Initialize CountVectorizer and vectorize all sentences
    vectorizer = TfidfVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    X = vectorizer.fit_transform(sentences)

    # Apply DBSCAN clustering
    cluster_labels = DBSCAN(eps=0.3, min_samples=1, metric='cosine',n_jobs=-1).fit_predict(X)

    # Store sentences in clusters
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        if label == -1:
            continue
        clusters.setdefault(label, []).append(queries[idx])

    # Convert to list of clusters and save as JSON
    clusters_list = list(clusters.values())

    test = {c["query"]:c["cluster"] for c in openJson("test.json")}
    final = []
    for cluster in clusters_list:
        f = {"queries":[],"cluster":set()}
        for title in cluster:
            f["queries"].append(title)
            for i in test[title]:
                f["cluster"].add(i)
        final.append(f)

    writeJson("clusters.json",final)

    print("Clusters saved to clusters.json")


def HDBSCAN():
    ""
    import hdbscan
    from sklearn.feature_extraction.text import CountVectorizer
    import json

    # Example list of sentences
    sentences = [c["query"] for c in openJson("test.json")]

    # Initialize CountVectorizer and vectorize all sentences
    vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    X = vectorizer.fit_transform(sentences)

    # Apply HDBSCAN clustering
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2, metric='cosine')
    cluster_labels = clusterer.fit_predict(X)

    # Store sentences in clusters
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        if label == -1:
            continue  # Skip noise points
        clusters.setdefault(label, []).append(sentences[idx])

    # Convert to list of clusters and save as JSON
    clusters_list = list(clusters.values())
    writeJson("clusters.json",clusters_list)

    print("Clusters saved to clusters.json")


def OPTICS():
    ""
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.cluster import OPTICS
    import json

    # Example list of sentences
    sentences = [c["query"] for c in openJson("test.json")]

    # Initialize CountVectorizer and vectorize all sentences
    vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    X = vectorizer.fit_transform(sentences)

    # Apply OPTICS clustering
    optics = OPTICS(min_samples=2, metric='cosine',n_jobs=-1)
    cluster_labels = optics.fit_predict(X)

    # Store sentences in clusters
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        if label == -1:
            continue  # Skip noise points
        clusters.setdefault(label, []).append(sentences[idx])

    # Convert to list of clusters and save as JSON
    clusters_list = list(clusters.values())
    writeJson("clusters.json",clusters_list)

    print("Clusters saved to clusters.json")


def AglomerativeClustering():
    ""

    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.cluster import AgglomerativeClustering
    import json

    # Example list of sentences
    sentences = [c["query"] for c in openJson("test.json")]

    # Initialize CountVectorizer and vectorize all sentences
    vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    X = vectorizer.fit_transform(sentences).toarray()  # AgglomerativeClustering requires dense input

    # Apply Agglomerative Clustering
    clustering = AgglomerativeClustering(n_clusters=None,distance_threshold=0.5, metric="cosine", linkage='average')
    cluster_labels = clustering.fit_predict(X)

    # Store sentences in clusters
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        clusters.setdefault(label, []).append(sentences[idx])

    # Convert to list of clusters and save as JSON
    clusters_list = list(clusters.values())
    writeJson("clusters.json",clusters_list)

    print("Clusters saved to clusters.json")


def AffinityPropagation():
    ""
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.cluster import AffinityPropagation
    from sklearn.metrics.pairwise import cosine_similarity
    import json

    # Example list of sentences
    sentences = [c["query"] for c in openJson("test.json")]

    # Initialize CountVectorizer and vectorize all sentences
    vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    X = vectorizer.fit_transform(sentences)

    # Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(X)

    # Define a similarity threshold
    threshold = 0.5

    # Create an affinity matrix with values above the threshold
    affinity_matrix = (similarity_matrix >= threshold).astype(float)

    # Apply Affinity Propagation
    affinity_propagation = AffinityPropagation(affinity='precomputed')
    cluster_labels = affinity_propagation.fit_predict(affinity_matrix)

    # Store sentences in clusters
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        clusters.setdefault(label, []).append(sentences[idx])

    # Convert to list of clusters and save as JSON
    clusters_list = list(clusters.values())
    writeJson("clusters.json",clusters_list)

    print("Clusters saved to clusters.json")