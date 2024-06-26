import time

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
    vectorizer = TfidfVectorizer(ngram_range=(3, 3), stop_words=None, lowercase=True, analyzer="char")
    getDataVizualisation(vectorizer,studiedOrigins=["press"],number = 8)

    end = time.time()
    print(f"executed in {round(end - start,2)}")