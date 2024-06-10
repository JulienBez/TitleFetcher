import json
import pyalex
from pyalex import Works
from itertools import chain

pyalex.config.email = "julien.bezancon@sorbonne-universite.fr"

#search by topics id
#query = Works().filter(topics = {"primary_topic" : {"id" : 17}})
#id = 17 = computer science
#id = 1702 = Artificial Intelligence

#search by primary topic
query = Works().filter(primary_topic = {"id" : "https://openalex.org/T10028"})

#search by seed
#query = Works().filter(title={"search" : "Climbing towards NLU On meaning form and understanding in the age of data"}) # only title with exact match, can't finde UMWEs candidates this way
#la query au dessus est utilisée pour trouver l'id du NLP

# 'field': {'id': 'https://openalex.org/fields/17', 'display_name': 'Computer Science'}
# 'primary_topic': {'id': 'https://openalex.org/T10028', 'display_name': 'Natural Language Processing'
# 'language': 'en'

dict_papers = {}

for record in chain(*query.paginate(per_page=200)):

    if record["id"] not in dict_papers:
        dict_papers[record["id"]] = {}

    if record["language"] not in  dict_papers[record["id"]]:
        dict_papers[record["id"]][record["language"]] = record["title"]

with open('data/test.json', 'w',encoding="utf'8") as f:
    json.dump(dict_papers, f, indent=4, ensure_ascii=False)

