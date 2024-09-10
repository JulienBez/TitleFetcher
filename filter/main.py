from src.navigation import *
from src.languages import *
from src.metadata import *
from src.minhasher import *
from src.filters import *
from src.clustering import *

if __name__ == "__main__":

    start = time.time()


    language = "fr"
    num_perm = 256
    ngram_range = (3,3)
    threshold = 0.5

    path = f"output/{language}_{num_perm}_{'-'.join([str(i) for i in ngram_range])}_{threshold}.json"
    
    #getLSHCluster(language,threshold=threshold,num_perm=num_perm,ngram_range=ngram_range)
    #getHeadClusters(path)
    #dropLessCoherent("test.json",threshold=0.6)

    #findSimilarLSHClusters(language,threshold=threshold,num_perm=num_perm,ngram_range=ngram_range)

    mergeClusters(language,threshold=threshold,num_perm=num_perm,ngram_range=ngram_range)

    a = openJson("a.json")

    import re
    new_a = {}
    for i,j in tqdm(a.items()):
        verif = [re.sub('\d', '#', k) for k in j]
        if len(set(verif)) > len(j)/2:
            new_a[i] = j
    
    writeJson("new_a.json",new_a)
    a = new_a
    #

    """
    counters = {}
    thresholds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

    for i in a:
        coherence = i["coherence"]
        for j in range(len(thresholds)-1):
            if coherence >= thresholds[j] and coherence < thresholds[j+1]:
                count = str(thresholds[j])+"-"+str(thresholds[j+1])
                if count not in counters:
                    counters[count] = 0
                counters[count] += len(i["cluster"])

    print(counters)
    """
    #

    print(len(a))
    
    b = 0
    c = 0

    new_new_a = {}

    for k,v in a.items():
        if len(v) > 2:
            b += len(v)
            new_new_a[k] = v
        else:
            c += 1

    print(b)
    print(c)   
    writeJson("new_new_a.json",new_new_a)

    #DBSCAN() #too bad
    #Aglomerative() #too long
    #HDBSCAN() #too much ram
    #OPTICS() #too long
    #AffinityPropagation() #too much ram

    #applyLanguageSpecificFilters("test.json")
    #dropLowClusters("test.json")
    #dropTooCoherent("test.json")

    end = time.time()
    print(f"executed in {round(end - start,2)}")