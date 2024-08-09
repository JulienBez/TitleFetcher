from src.navigation import *
from src.languages import *
from src.metadata import *
from src.hasher import *

if __name__ == "__main__":

    start = time.time()

    getLSHCluster(["movie"],1,treshold=0.5,num_per=256,ngram_range=(3,3))
    getCoherenceMeasure("data/clusters/fr/movie/LSH_treshold0.5_numper256_ngram3-3.json")
    dropLessCoherent("data/clusters/fr/movie/LSH_treshold0.5_numper256_ngram3-3.json",thresold=0.5)

    t,_ = getTitles("fr",["movie"])
    print(len(t))

    a = openJson("test.json")
    print(len(a))
    
    counter = 0
    for i in a:
        counter += len(i["cluster"])
    print(counter)

    
    ###

    c = 0
    for j in a:
        if j["coherence"] >= 0.9 or len(j["cluster"]) <= 4:
            c += 1
    print("candidats elimination : ",c)
    
    ###

    
    cyes = 0
    cno = 0

    tyes = 0
    tno = 0

    syes = set()
    sno = set()

    for i in a:
        if i["coherence"] >= 0.5:
            cyes += 1
            tyes += len(i["cluster"])
            for j in i["cluster"]:
                syes.add(j)
        else:
            cno += 1
            tno += len(i["cluster"])
            for j in i["cluster"]:
                sno.add(j)

    print(cyes,"\t",tyes,"\t",len(syes))
    print(cno,"\t",tno,"\t",len(sno))

    correct = set(sum([[i.lower() for i in j]for j in openJson("sample.json")],[]))
    print(len(syes.intersection(correct)),"/",len(correct))

    sno_fix = sno.difference(syes)

    print(len(sno.intersection(correct)),"/",len(correct))
    print(len(sno_fix.intersection(correct)),"/",len(correct))

    writeJson('no_fix.json',list(sno_fix.intersection(correct)))

    def dropDuplicates(path):
        ""
        data = [set(i["cluster"]) for i in openJson(path)]
        frozensets = set(frozenset(s) for s in data)
        uniques = [list(set(fs)) for fs in frozensets]
        writeJson("testfroz.json",uniques)

    dropDuplicates('test.json')
    data = openJson("testfroz.json")
    print(len(data))

    ###

    liste_voc = []

    end = time.time()
    print(f"executed in {round(end - start,2)}")