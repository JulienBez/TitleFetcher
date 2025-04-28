from .navigation import *

from Bio.Seq import Seq
from Bio import pairwise2


def deleteBadAlignments(cluster):
    """sometime we align two different words between the seed and the sent, we remove those occurrences"""
    for entry in cluster:
        new_alignments = []
        for alignments in entry["alignments"]:
            erroned = False
            for i,w in enumerate(alignments[0]):
                if w != "-" and alignments[1][i] != "-" and w != alignments[1][i]:
                    erroned = True
            if not erroned:
                new_alignments.append(alignments)
        entry["alignments"] = new_alignments
    writeJson(path,data)


def alignment(seed,sent):
    """align a seed and a sent using Biopython function"""
    alignments = pairwise2.align.globalms(sent,seed,2,-1,-0.5,-0.1, gap_char=["-"]) #biopython function, only gap_char matters here
    return [[align[0],align[1]] for align in alignments] #0 and 1 indexes are aligned list in returned biopython object


def align(cluster):
    """for each sent in json (path), tokenize this sent and align it with its seed"""
    list_align = []
    query = cluster["query"].split(" ")
    for entry in cluster["cluster"]:
        list_align.append(alignment(query,entry.split(" "))[0])
    return list_align


def exactSegment(seed_align):
    """we ignore misalignment lists"""
    return sorted([i for i in seed_align if type(i) == int])


def commonSegment(seed,sent):
    """common segment isolation between a seed and a sent using list comprehension"""

    #to vizualise multiple tokens substitution (example with "Max a cassé sa pipe" and "Max a bien dégommé sa pipe")
    seed_align = [] #[0, 1, ['casser'], 4, 5]
    sent_align = [] #[0, 1, ['bien', 'dégommer'], 4, 5]
    #we see that 'casser' is replaced by either 'bien' or 'dégommer' if we only take into account our alignments

    #to create the sublists ["casser"] and ["bien","dégommer"]
    seed_subalign = []
    sent_subalign = []

    #to find the true ids of words in sent and seed, the one they had before alignment
    sep_counter_seed = 0
    sep_counter_sent = 0
    
    index_counter = 0 #we want to retrieve the indexes of the original sentence, so we increment this variable when needed only
    for i in range(len(seed)): #for each element in our alignments...

        if sent[i] == seed[i]: #if its a match

            #we add the sublists if there are misaligned elements
            if seed_subalign and sent_subalign:
                seed_align.append(seed_subalign)
                sent_align.append(sent_subalign)

            #we note the index of the match for both lists
            seed_align.append(index_counter-sep_counter_seed)
            sent_align.append(index_counter-sep_counter_seed) #very important, I struggled with this one for some reason

            #we reset our sublists in case of match, to get ready to create others sublists
            seed_subalign = []
            sent_subalign = []

            index_counter += 1 #we take a step

        if sent[i] == "-" and seed[i] != "-": #if there is an element of the seed we can't find in the sent
            #seed_subalign.append(seed[i])
            sep_counter_seed += 1
            seed_subalign.append(i-sep_counter_sent)
            index_counter += 1

        if sent[i] != "-" and seed[i] == "-": #if there is an element of the sent we can't find in the seed
            #sent_subalign.append(sent[i])
            sep_counter_sent += 1
            sent_subalign.append(i-sep_counter_seed)
            index_counter += 1

    if seed_subalign and sent_subalign: #to fetch the last terms 
        seed_align.append(seed_subalign)
        sent_align.append(sent_subalign)

    return seed_align

    #if len(sent_align) > 1 and len(seed_align) > 1:
    #    return exactSegment(seed_align)
    
    #else:
    #    return ""

def findSnowclone(path):
    ""
    data = openJson(path)
    results_all = []

    for cluster in data[22200:22400]:

        list_align = align(cluster)
        query = cluster["query"].split(" ")
        results_cluster = []

        #retrieve the patterns for each title
        for a in list_align:
            indexes = commonSegment(a[0],a[1])
            aligned = []
            for i in indexes:
                try:
                    if type(i)==int:
                        aligned.append(query[i])
                    else:
                        aligned.append("X")
                except:
                    aligned.append("X")
            results_cluster.append(aligned)


        for k in results_cluster:
            print(k)
        print(" ")
        
