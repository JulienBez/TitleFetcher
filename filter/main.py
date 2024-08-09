from src.navigation import *
from src.languages import *
from src.metadata import *
from src.minhasher import *

if __name__ == "__main__":

    start = time.time()


    language = "fr"
    num_perm = 256
    ngram_range = (3,3)
    threshold = 0.5

    path = f"output/{language}_{num_perm}_{'-'.join([str(i) for i in ngram_range])}_{threshold}.json"
    
    #getLSHCluster("fr",threshold=0.5,num_perm=256,ngram_range=(3,3))
    getHeadClusters(path)
    dropLessCoherent("test.json",threshold=0.4)



    end = time.time()
    print(f"executed in {round(end - start,2)}")