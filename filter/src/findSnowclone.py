from .navigation import *

from collections import Counter


def filterPatterns(path):
    data = openJson(path)
    new_data = []
    for pattern in data:
        pat = pattern[1].split(" ")
        with_X = [i for i in pat if i == "X"]
        if len(with_X) < len(pat)/3:
            new_data.append(pattern)
    print(len(new_data))
    writeJson(path,new_data)


def findSnowclone(path):
    ""
    
    data = openJson(path)
    all_patterns = {}

    for cluster in tqdm(data):

        #print("### ",cluster["query"]," ###")
        
        cluster_clean = [c.lower().split(" ") for c in cluster["cluster"]]
        mean_length = max([(v,k) for k,v in Counter([len(i) for i in cluster_clean]).items()])[1]
        cluster = [c for c in cluster_clean if len(c) == mean_length]
        
        pattern = []
        for i in range(mean_length):
            position = []

            for seq in cluster:
                position.append(seq[i])

            #print(position)
            best_guess = max([[v,k] for k,v in Counter(position).items()])

            if best_guess[0] > len(position)/2:
                pattern.append(best_guess[1])

            else:
                pattern.append("X")
        
        pattern = " ".join(pattern)
        if pattern not in all_patterns:
            all_patterns[pattern] = 0
        all_patterns[pattern] += len(cluster_clean)

    print(len(all_patterns))
    writeJson("tetest.json",sorted([[v,k] for k,v in all_patterns.items()],reverse=True))
