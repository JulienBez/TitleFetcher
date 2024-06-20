import os

from .navigation import *

import time

def DBSCANSubsetsClustering():

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