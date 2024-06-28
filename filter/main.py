from src.navigation import *
from src.languages import *
from src.clustering import *
from src.metadata import *

if __name__ == "__main__":

    start = time.time()

    #languageStep()
    #clusterAnalyzer()
    #getBasicMetadatas()
    #getDataVizualisation(studiedOrigins=["movie"])
    #getBasicMetadatasHistogram(logscale=False)
    
    #vectorizer = TfidfVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    #getDataVizualisation(vectorizer,studiedOrigins=["press"],number = 8)
    #dataVisualisationLoop(studiedOrigins=["movie","paper","press"],number=8)

    genres = ["press","movie","paper"]
    number = 8

    dataVisualisationLoop(genres,number)

    vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words=None, lowercase=True, analyzer="char")

    getVizualisation(vectorizer,genres,number)
    KMeansClustering(vectorizer,genres,number)
    getVizualisation(vectorizer,genres,number,clusters=True)

    getGenresPerClusters(vectorizer,genres,number,"Kmeans")

    end = time.time()
    print(f"executed in {round(end - start,2)}")