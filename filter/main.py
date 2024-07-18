from src.navigation import *
from src.languages import *
from src.clustering import *
from src.metadata import *

from src.hasher import *

if __name__ == "__main__":

    start = time.time()

    #languageStep()
    #print("basic metadatas...")
    #getBasicMetadatas()
    #getBasicMetadatasHistogram(logscale=True)
    #getBasicMetadatasHistogram(logscale=False)

    #getLSHCluster(["movie"],1,treshold=0.4,num_per=256,ngram_range=(3,3))
    getCoherenceMeasure("data/clusters/fr/movie/LSH_treshold0.4_numper256_ngram3-3.json")
    #getCoherenceMeasure("autosampleTEST.json")
    #dropLessCoherent("data/clusters/fr/movie/LSH_treshold0.4_numper256_ngram3-3.json",thresold=0.4)
    #data = mergeSimilarClusters(openJson("test.json"),intersection=0.5)
    #writeJson("test.json",data)
    
    #data = openJson("data/clusters/fr/movie/LSH_treshold0.4_numper256_ngram3-3.json")
    #new_data = [i["cluster"] for i in data]
    #writeJson("data/clusters/fr/movie/LSH_treshold0.4_numper256_ngram3-3.json",new_data)

    #autosample = sum(openJson("autosample_final.json"), [])

    ############################################

    #data = openJson("sample.json")
    #data = [list(set([a.lower() for a in d])) for d in data]
    #print(len(data))
    #writeJson("sample_clean.json",data)

    # LSH CLUSTERS #

    #genres = ["movie"]
    #number = 9

    #print("LSH clusters...")

    #treshold = [0.3,0.4,0.5,0.6,0.7]
    #num_per = [256]
    #ngram_range = [(2,2),(3,3),(2,3)]

    #counter = 0
    #total = len(treshold) * len(num_per) * len(ngram_range)

    #for n in ngram_range:
    #    for p in num_per:
    #        for t in treshold:
    #            pathy = f"data/clusters/fr/{('_').join(genres)}/LSH_treshold{t}_numper{p}_ngram{'-'.join([str(i) for i in n])}.json"
    #            if not os.path.exists(pathy):
    #                getLSHCluster(genres,number,treshold=t,num_per=p,ngram_range=n)
    #            counter += 1
    #            print(f"\033[2K\r{counter}/{total}", end='', flush=True)

    #data = openJson("data/clusters/fr/movie/LSH_treshold0.4_numper256_ngram2-3.json")
    #print(len(data))
    #new_data = []
    #total = 0  
    #for i in data:
    #    if len(i) > 1:
    #        new_data.append(i)
    #        total += len(i)
    #print(len(new_data))
    #print(total)

    #writeJson("test.json",new_data)
    #new_new_data = openJson("test2.json")
    #writeJson("test3.json",mergeSimilarClusters(new_new_data,intersection=0.2))
    
    #writeJson("test.json",sorted(new_data, key=len, reverse=True))

    # CLUSTERISATION #

    #vectorizer = TfidfVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")

    #print("first vizualisation...")
    #getVizualisation(vectorizer,genres,number)

    #print("KMeans...")
    #KMeansClustering(vectorizer,genres,number)
    #getVizualisation(vectorizer,genres,number,clusters=True,clusterType="KMeans")
    #getGenresPerClusters(vectorizer,genres,number,clusterType="KMeans")

    #print("DBscan...")
    #DBscanClustering(vectorizer,genres)
    #getVizualisation(vectorizer,genres,number,clusters=True,clusterType="DBscan")
    #getGenresPerClusters(vectorizer,genres,number,clusterType="DBscan")

    end = time.time()
    print(f"executed in {round(end - start,2)}")