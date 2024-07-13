import numpy as np
from hashlib import sha1
from datasketch.lsh import MinHashLSH
from datasketch.minhash import MinHash

from .navigation import *

def makeQuery(title,lsh,num_per,ngram_range):
    ""
    minhash = MinHash(num_perm=num_per)
    ngram_title = set()
    for ngram in ngram_range:
        ngram_title.update([title[i:i+ngram] for i in range(len(title)-1)])
    for ntitle in ngram_title:
        minhash.update(ntitle.encode('utf-8'))
    return lsh.query(minhash)


def getMinhashes(language,genres,titles,treshold,num_per,ngram_range):
    ""

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


def getLSHCluster(genres,number,treshold=0.5,num_per=128,ngram_range=(2,3)):
    ""

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
            titles.difference_update(set(res_query)) #on retire des queries tous les éléments qu'on a déjà vu au moins une fois pour accélérer la procédure

        writeJson(f"data/clusters/{lang}/{('_').join(genres)}/LSH_treshold{treshold}_numper{num_per}_ngram{'-'.join([str(i) for i in ngram_range])}.json",res)


def mergeSimilarClusters(clusters,intersection=0.5):
    ""

    merged_sets = []
    set_clusters = [set(c) for c in sorted(clusters, key=len)]

    while set_clusters:

        to_remove = []
        pointer = set_clusters[0]

        for i in range(1, len(set_clusters)):

            intersection_size = len(pointer.intersection(set_clusters[i]))
            min_size = min(len(pointer), len(set_clusters[i]))

            if intersection_size >= intersection * min_size:
                pointer.update(set_clusters[i])
                to_remove.append(i)

        merged_sets.append(pointer)
        
        for ind in sorted(to_remove,reverse=True):
            del set_clusters[ind]
        del set_clusters[0]

        print(f"\033[2K\r{len(set_clusters)}", end='', flush=True)

    return [list(ms) for ms in merged_sets]

