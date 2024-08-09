import itertools
import numpy as np
from hashlib import sha1
from joblib import Parallel, delayed
from datasketch.lsh import MinHashLSH
from datasketch.minhash import MinHash
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from .navigation import *

def makeQuery(title,lsh,num_per,ngram_range):
    "make a query using a given title and lsh parameters"
    minhash = MinHash(num_perm=num_per)
    ngram_title = set()
    for ngram in ngram_range:
        ngram_title.update([title[i:i+ngram] for i in range(len(title)-1)])
    for ntitle in ngram_title:
        minhash.update(ntitle.encode('utf-8'))
    return lsh.query(minhash)


def getMinhashes(language,genres,titles,treshold,num_per,ngram_range):
    "create a lsh index with specified parameters and save it if not exist"
    createFolder("data/minhashes")
    createFolder(f"data/minhashes/{language}")
    pathLSH = f"data/minhashes/{language}/{language}_treshold{treshold}_numper{num_per}_ngram{'-'.join([str(i) for i in ngram_range])}_{('_').join(genres)}.lsh"
    if not os.path.isfile(pathLSH):
        lsh = MinHashLSH(threshold=treshold, num_perm=num_per)
        for title in titles:
            ngram_title = set()
            for ngram in ngram_range:
                ngram_title.update(set([title.lower()[i:i+ngram] for i in range(len(title)-1)]))
            minhash = MinHash(num_perm=num_per)        
            for ntitle in ngram_title:
                minhash.update(ntitle.encode('utf-8'))
            lsh.insert(title, minhash)
        writeVector(pathLSH,lsh) 
    else:
        lsh = openVector(pathLSH)
    return lsh


def getLSHCluster(genres,number,treshold=0.4,num_per=256,ngram_range=(3,3)):
    "make queries over lsh index to create clusters"
    createFolder("data/clusters")
    dict_languages = openJson("logs/dict_languages.json")
    sorted_dict_languages = [i[0] for i in sorted(dict_languages.items(), key=lambda x:x[1],reverse=True)]
    for lang in ["fr"]:
    #for lang in tqdm(sorted_dict_languages[1:number-1]):
        createFolder(f"data/clusters/{lang}")
        createFolder(f"data/clusters/{lang}/{('_').join(genres)}")
        titles, origins = getTitles(lang,genres)
        titles = set(titles)
        lsh = getMinhashes(lang,genres,titles,treshold,num_per,ngram_range)
        res = []
        while titles:
            res_query = makeQuery(titles.pop(),lsh,num_per,ngram_range)
            res.append(res_query)
            #titles.difference_update(set(res_query)) #remove titles with saw at least 1 time to reduce the number of clusters
        writeJson(f"data/clusters/{lang}/{('_').join(genres)}/LSH_treshold{treshold}_numper{num_per}_ngram{'-'.join([str(i) for i in ngram_range])}.json",res)


def coherenceMeasure(cluster):
    "vectorize each possible pair in a cluster to get a list of cosine similarity, then get mean of this list"
    try:
        vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
        X = vectorizer.fit_transform(cluster)
        cosine_sim = cosine_similarity(X)
        total = list(itertools.chain(*cosine_sim))
        return (sum(total)-len(cluster))/(len(total)-len(cluster)) # -len(cluster) to remove diagonals in cosine similarity matrice
    except:
        return 0.0


def coherenceMeasureBIS(cluster):
    ""
    vectorizer = TfidfVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    allCos = []
    for i in range(len(cluster)-1):
        try:
            X = vectorizer.fit_transform([cluster[i],cluster[i+1]])
            simCos = cosine_similarity(X[0:1], X[1:2])[0][0]
            allCos.append(simCos)
        except:
            allCos.append(0.0)
    return sum(allCos)/len(allCos)


def sortByCoherence(clusters, n_jobs=-1):
    "parallel processing of coherence measure over all clusters"
    cluster_similarities = Parallel(n_jobs=n_jobs)(
        delayed(lambda cluster: {"cluster": cluster, "coherence": coherenceMeasure(cluster)})
        (cluster)
        for cluster in clusters
        )    
    sorted_clusters = sorted(cluster_similarities, key=lambda x: x["coherence"], reverse=True)
    return sorted_clusters


def getCoherenceMeasure(path):
    ""
    data = openJson(path)
    new_data = []
    for cluster in data:
        cluster_clean = list(set([c.lower() for c in cluster])) #remove noise, aka clusters with same titles when lower() applied
        if len(cluster_clean) > 1: #remove uninteressting clusters
            new_data.append(cluster_clean)
    writeJson(path,sortByCoherence(new_data))


def dropLessCoherent(path,thresold=0.4):
    ""
    data = openJson(path)
    new_data = []
    for cluster in data:
        if cluster["coherence"] >= thresold:
            new_data.append(cluster)
    print(f"initial number of clusters : {len(data)}")
    print(f"number of clusters after dropLessCoherent filter : {len(new_data)}")
    writeJson("test.json",new_data)


def mergeSimilarClusters(clusters,intersection=0.5):
    "merge similar clusters to avoid redondance"

