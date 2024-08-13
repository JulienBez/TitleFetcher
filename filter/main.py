from src.navigation import *
from src.languages import *
from src.metadata import *
from src.minhasher import *
from src.filters import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN
import json


start = time.time()

# Example list of sentences
sentences = [c["query"] for c in openJson("test.json")]

# Initialize CountVectorizer and vectorize all sentences
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)

# Apply DBSCAN clustering
cluster_labels = DBSCAN(eps=0.2, min_samples=1, metric='cosine',n_jobs=-1).fit_predict(X)

# Store sentences in clusters
clusters = {}
for idx, label in enumerate(cluster_labels):
    if label == -1:
        continue
    clusters.setdefault(label, []).append(sentences[idx])

# Convert to list of clusters and save as JSON
clusters_list = list(clusters.values())
with open("clusters.json", "w") as f:
    json.dump(clusters_list, f, indent=4)

print("Clusters saved to clusters.json")

end = time.time()
print(f"executed in {round(end - start,2)}")

if __name__ == "__main__":

    start = time.time()


    language = "fr"
    num_perm = 256
    ngram_range = (3,3)
    threshold = 0.5

    path = f"output/{language}_{num_perm}_{'-'.join([str(i) for i in ngram_range])}_{threshold}.json"
    
    #getLSHCluster(language,threshold=threshold,num_perm=num_perm,ngram_range=ngram_range)
    #getHeadClusters(path)

    #dropLessCoherent("test.json")
    #applyLanguageSpecificFilters("test.json")

    #dropLowClusters("test.json")
    
    
    #getQueryClusters("test.json")

    end = time.time()
    print(f"executed in {round(end - start,2)}")