from sentence_transformers import SentenceTransformer, util

from .navigation import *

import time


#https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/fast_clustering.py
def test2():

    #TODO1 : au lieu de faire ça on peut faire [ [id,titre,langue,origine], [id,titre,langue,origine], ... ]
    titles = set()
    #for path in glob.glob("data/languages/fr/*.json"):
    for path in glob.glob("data/frtest/*.json"):
        data = openJson(path)
        for k,v in data.items():
            titles.add(v["title"])
    titles = list(titles) #TODO1 : et là on fait titles = [i[1] for i in notre_liste]

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

    dict_cluster = {}
    for i, cluster in enumerate(clusters):
        print("Cluster {}, #{} Elements ".format(i , len(cluster)))
        if str(i) not in dict_cluster:
            dict_cluster[str(i)] = []
        for sentence_id in cluster:
            dict_cluster[str(i)].append(titles[sentence_id])
    writeJson("test.json",dict_cluster)