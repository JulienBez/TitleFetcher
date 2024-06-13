#check if we scrapped twice or more the same page

import json

with open('logs/metadata_2020.json','r',encoding="utf-8") as f:
    metadata = json.load(f)

values = []
for k,v in metadata.items():
    if v not in values:
        values.append(v)
    else:
        print(v)