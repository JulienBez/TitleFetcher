import re
import string as strii
from collections import Counter

from .navigation import *

## Generic filters - should be fine for all languages ##

def getHeadClusters(path):  #étape clé : REGARDER CE QU'ON VIRE AVEC, VIRE-T-ON DES CLUSTERS INTERESSANTS ? SI OUI, FAIRE LE MERGE PLUTOT MEME SI LONG
    "for each title, find the cluster with the best coherence score containing this title"
    clusters = openJson(path)
    map = {}
    for i,cluster in enumerate(clusters):
        for title in cluster["cluster"]:
            if title not in map:
                map[title] = i
    new_clusters = [clusters[idx] for idx in set([v for k,v in map.items()])]
    print(f"initial number of clusters : {len(clusters)}")
    print(f"number of clusters after getHeadClusters filter : {len(new_clusters)}")
    writeJson("test.json",new_clusters)


def dropLessCoherent(path,threshold=0.5):
    ""
    clusters = openJson(path)
    new_clusters = []
    for cluster in clusters:
        if cluster["coherence"] >= threshold:
            new_clusters.append(cluster)
    print(f"initial number of clusters : {len(clusters)}")
    print(f"number of clusters after dropLessCoherent filter : {len(new_clusters)}")
    writeJson("test.json",new_clusters)


def dropTooCoherent(path,threshold=0.9):
    clusters = openJson(path)
    new_clusters = []
    for cluster in clusters:
        if cluster["coherence"] < threshold:
            new_clusters.append(cluster)
    print(f"initial number of clusters : {len(clusters)}")
    print(f"number of clusters after dropTooCoherent filter : {len(new_clusters)}")
    writeJson("test.json",new_clusters)


def dropLowClusters(path,threshold=3):
    ""
    clusters = openJson(path)
    new_clusters = []
    for cluster in clusters:
        if len(cluster["cluster"]) >= threshold:
            new_clusters.append(cluster)
    print(f"initial number of clusters : {len(clusters)}")
    print(f"number of clusters after dropLowClusters filter : {len(new_clusters)}")
    writeJson("test.json",new_clusters)


def dropByLongestCommonString(path):
    ""
    clusters = openJson(path)
    new_clusters = []
    for cluster in clusters:
        pass

## Language revelant filter - use them according to the studied language ##

def removeNumbers(cluster):
    ""
    return [re.sub(r'\d+'," ",c) for c in cluster]


def removeCases(cluster):
    ""
    return [c.lower() for c in cluster]


def removePunctuations(cluster):
    ""
    return [c.translate(str.maketrans({key: " {0} ".format(key) for key in strii.punctuation})) for c in cluster]


def removeLargeSpaces(cluster):
    ""
    return [re.sub(' +',' ',c) for c in cluster]


def applyLanguageSpecificFilters(path,numbers=True,cases=True,punctuation=True):
    ""
    clusters = openJson(path)
    new_clusters = []
    for cluster in clusters:
        cluster_clean = cluster["cluster"]
        if numbers:
            cluster_clean = removeNumbers(cluster_clean)
        if cases:
            cluster_clean = removeCases(cluster_clean)
        if punctuation:
            cluster_clean = removePunctuations(cluster_clean)
        cluster_clean = removeLargeSpaces(cluster_clean)
        maxi = Counter(cluster_clean).most_common(1)[0][1]
        if maxi/len(cluster) < 0.9:
            new_clusters.append(cluster)
    print(f"initial number of clusters : {len(clusters)}")
    print(f"number of clusters after applyLanguageSpecificFilters filter : {len(new_clusters)}")
    writeJson("test.json",new_clusters)


#avant de drop les clusters les moins cohérents : 
# pour chaque cluster, récupérer la query qui a donné ce cluster
# on recherche les cluster heads
# pour chaque cluster head, on récupère sa query
# on clusterise les queries sur du DBSCAN en récupérant les ids à la fin du clustering
# on merge les clusters originaux (avant DBSCAN) à l'aide des clusters d'ids obtenus avec les queries
# peut-être faire un dropLessCoherent avant pour avoir - de queries à clusteriser

# on peut améliorer le process en recherchant au préalable les queries renvoyant au moins 1 résultat similaire -> on divise nos queries en petits groupes
#faire droplesscoherent et droplowcluster avant de faire clusterhead