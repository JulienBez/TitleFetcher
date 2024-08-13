import itertools
from hashlib import sha1
from joblib import Parallel, delayed
from datasketch.lsh import MinHashLSH
from datasketch.minhash import MinHash
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from .navigation import *

def getTitles(language):
    "get all titles for a given language and save them in a dict"
    "for each title, save a list of all ids with this title"
    createFolder("data/dictionnaries")
    titlePath = f"data/dictionnaries/dict_{language}.json"
    if not os.path.isfile(titlePath):
        titles = {}
        for path in glob.glob(f"data/languages/{language}/*.json"):
            data = openJson(path)
            for key,value in data.items():
                if value["title"] not in titles:
                    titles[value["title"]] = []
                titles[value["title"]].append(key)
        writeJson(titlePath,titles)
    else:
        titles = openJson(titlePath)
    return list(titles.keys())


def getMinhash(title,num_perm,ngram_range):
    "hashes a title given a specific number of permutations and a ngram range"
    minhash = MinHash(num_perm=num_perm)
    ngram_title = set()
    for ngram in ngram_range:
        ngram_title.update(set([title.lower()[i:i+ngram] for i in range(len(title)-1)]))
    for ntitle in ngram_title:
        minhash.update(ntitle.encode('utf-8'))
    return minhash


def parallelGetMinhash(language,num_perm,ngram_range,n_jobs=-1):
    "execute getMinhash over a list of titles with parallel processing"
    createFolder("data/minhashes")
    minhash_path = f"data/minhashes/{language}_{num_perm}_{'-'.join([str(i) for i in ngram_range])}.lsh"
    if not os.path.exists(minhash_path):
        titles = getTitles(language)
        print(f"creating minhashes for {language}")
        minhash_dict = Parallel(n_jobs=n_jobs,backend='loky')(
            delayed(getMinhash)(title,num_perm,ngram_range) for title in tqdm(titles)
        )
        minhash_dict = {titles[i]:m for i,m in enumerate(minhash_dict) if m is not None}
        writeBin(minhash_path,minhash_dict)
    else:
        minhash_dict = openBin(minhash_path)
    return minhash_dict


def getCoherence(cluster):
    "vectorize each possible pair in a cluster to get a list of cosine similarity, then get mean of this list"
    try:
        vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
        X = vectorizer.fit_transform(cluster)
        cosine_sim = cosine_similarity(X)
        total = list(itertools.chain(*cosine_sim))
        return (sum(total)-len(cluster))/(len(total)-len(cluster)) # -len(cluster) to remove diagonals in cosine similarity matrice
    except:
        return 0.0


def parallelGetCoherence(language,clusters,n_jobs=-1):
    "parallel processing of coherence measure over all clusters"
    clusters = [cluster for cluster in clusters if len(list(set([c.lower() for c in cluster["cluster"]]))) > 1]
    print(f"calculating coherence measures for {language}")
    cluster_similarities = Parallel(n_jobs=n_jobs)(
        delayed(lambda cluster: {"query":cluster["query"],"cluster": cluster["cluster"], "coherence": getCoherence(cluster["cluster"])})
        (cluster) for cluster in tqdm(clusters))    
    sorted_clusters = sorted(cluster_similarities, key=lambda x: x["coherence"], reverse=True)
    return sorted_clusters


def getLSH(language,minhashes,threshold,num_perm):
    "create a LSH index with the specified threshold"
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    print(f"populating LSH index for {language}")
    for k,v in tqdm(minhashes.items()):
        lsh.insert(k,v)
    return lsh


def getLSHCluster(language,threshold=0.5,num_perm=256,ngram_range=(3,3)):
    "create a LSH index and create a cluster of similar titles for each title"
    createFolder("output")
    output_file = f"output/{language}_{num_perm}_{'-'.join([str(i) for i in ngram_range])}_{threshold}.json"
    minhashes = parallelGetMinhash(language,num_perm,ngram_range)
    lsh = getLSH(language,minhashes,threshold,num_perm)   
    clusters = []
    print(f"querying over the LSH index for {language}")
    for k,v in tqdm(minhashes.items()):
        clusters.append({"query":k,"cluster":list(set(lsh.query(v)))})
    writeJson(output_file,parallelGetCoherence(language,clusters))


def getQueryClusters(path):
    ""
    
    clusters = openJson(path)
    queries = [cluster["query"].lower() for cluster in clusters]
    
    from sklearn.cluster import Birch
    vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    X = vectorizer.fit_transform(queries).toarray()

    clustering = Birch(threshold=0.5,n_clusters=None)
    labels = clustering.fit_predict(X)

    clusters_dict = {}
    for query,label in zip(queries, labels):
        lab = str(label)
        if lab not in clusters_dict:
            clusters_dict[lab] = []
        clusters_dict[lab].append(query)

    writeJson("testqueries.json",clusters_dict)

#avant de drop les clusters les moins cohérents : 
# pour chaque cluster, récupérer la query qui a donné ce cluster
# on recherche les cluster heads
# pour chaque cluster head, on récupère sa query
# on clusterise les queries sur du DBSCAN en récupérant les ids à la fin du clustering
# on merge les clusters originaux (avant DBSCAN) à l'aide des clusters d'ids obtenus avec les queries
# peut-être faire un dropLessCoherent avant pour avoir - de queries à clusteriser

# on peut améliorer le process en recherchant au préalable les queries renvoyant au moins 1 résultat similaire -> on divise nos queries en petits groupes
#faire droplesscoherent et droplowcluster avant de faire clusterhead