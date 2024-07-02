from src.navigation import *
from src.languages import *
from src.clustering import *
from src.metadata import *

if __name__ == "__main__":

    start = time.time()

    #languageStep()
    #print("basic metadatas...")
    #getBasicMetadatas()
    #getBasicMetadatasHistogram(logscale=True)
    #getBasicMetadatasHistogram(logscale=False)
    
    #print("first vizualisation...")
    #vectorizer = TfidfVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    #getVizualisation(vectorizer,["paper"],8) #["movie","paper","press"]
    #dataVisualisationLoop(studiedOrigins=["movie","paper","press"],number=8)

    a,b = getTitles("en",["movie","paper","press"])
    print(len(a))
    1/0

    genres = ["movie"]
    number = 8

    #dataVisualisationLoop(genres,number)

    vectorizer = TfidfVectorizer(ngram_range=(3,3), stop_words=None, lowercase=True, analyzer="char")

    #getVizualisation(vectorizer,genres,number)
    KMeansClustering(vectorizer,genres,number)
    getVizualisation(vectorizer,genres,number,clusters=True)
    getGenresPerClusters(vectorizer,genres,number,"Kmeans")

    end = time.time()
    print(f"executed in {round(end - start,2)}")