import re
import os
import json

from imdb import Cinemagoer # https://cinemagoer.readthedocs.io/en/latest/ + https://www.octoparse.com/blog/how-to-scrape-imdb-data = droits pour scrapper IMDB ?
ia = Cinemagoer()

def openJson(path):
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data

def writeJson(path,data):
  with open(path,"w",encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)

def cleanList(liste):
    return [str(i) for i in liste]

if not os.path.isfile("output.json"):
       writeJson("output.json",[])

#initiation du programme
movie_list = ["John Wick","rec"]

for m in movie_list:

    #recherche pour chaque film 1 à 1
    sr = ia.search_movie(m)

    #tri des résultats de la recherche
    choices = [sr[0]] #on part du principe que le premier choix retourné est le bon
    for movie in sr[1:]:
        if re.search(m,movie['title']): #au cas où, on regarde si les autres choix sont viables
            choices.append(movie)

    #si on a plus d'un résultat
    if len(choices) > 1:

        #on a un menu de choix interractif
        print("Select all movies you want to add to the database as follow : 0,2,3,5\n")
        for i,c in enumerate(choices):
            print(f"{i} - {c}")
        print("\n")
        selection = [int(r) for r in input("Your selection : ").split(",")]
        
        #on retient les numéros désignés
        final = []
        for i in selection:
            final.append(choices[i])

    #si on a un résultat, étape suivante direct
    else:
       final = choices

    final_id = ids = [i.movieID for i in final]

    #enregistrement dans database
    for d in final_id:
        res = openJson("output.json")

        #choix des informations désirées
        try:

            movie = ia.get_movie(d)
            entry = {}
            for k,v in movie.items():
                if k not in entry:
                    entry[k] = v
                    if type(v) == list:
                        entry[k] = cleanList(v)
            
            if entry not in res:
                res.append(entry)
            writeJson("output.json",res)

        except KeyError:
            print(f"The following movie couldn't be added : {str(movie)}")
            pass

