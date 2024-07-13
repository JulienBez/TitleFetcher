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

    import re

    #regex = re.compile(r"et des hommes")
    #regex = re.compile(r"la face cachée")
    #regex = re.compile(r"il faut sauver l.*")
    #regex = re.compile(r"(liberté,)|(égalité,)|(fraternité)")
    #regex = re.compile(r"(le bon,)|(la brute et)|(la brute,)|(le truand)")
    #regex = re.compile(r"confessions? d.*")
    #regex = re.compile(r"malgré ")
    #regex = re.compile(r"l'appel ")
    #regex = re.compile(r"itinéraire d'un ")
    #regex = re.compile(r"le retour du ")
    #regex = re.compile(r"apocalypse \w*o\w*")
    #regex = re.compile(r"la tête dans ")
    #regex = re.compile(r"la guerre des \w*oi\w*")
    #regex = re.compile(r"l\w* cinquième ")
    #regex = re.compile(r"il était une fois\.\.\.")
    #regex = re.compile(r"il était \w* foi\w* ")
    #regex = re.compile(r"danse avec l\w*")
    #regex = re.compile(r"de contrôle")
    #regex = re.compile(r"coup d.*")
    #regex = re.compile(r".+ d'un soir")
    #regex = re.compile(r".+ de la discorde")
    #regex = re.compile(r"tant qu'il y aura")
    #regex = re.compile(r"l'\w+ est dans") #x2 MWEs ! 
    #regex = re.compile(r"l'\wge de")
    #regex = re.compile(r"\w+ de l'eau")
    #regex = re.compile(r"\w+ (du siècle)")
    #regex = re.compile(r"\w+ c'est \w+ un peu .*")
    #regex = re.compile(r"maman.*raté.*")
    regex = re.compile(r"contre-attaque")

    fr_titles,fr_genre = getTitles('fr',["movie"])

    autosample = openJson("autosample.json")
    candidates = []

    for title in fr_titles:
        if regex.search(title.lower()):
            candidates.append(title)

    autosample.append(candidates)
    writeJson("autosample.json",autosample)


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