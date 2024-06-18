import os
import json
import glob
import shutil
from tqdm import tqdm

def openJson(path):
  "open a json file"
  with open(path,'r',encoding='utf-8') as f:
    data = json.load(f)
  return data
  

def writeJson(path,data):
  "create a json file"
  with open(path,"w",encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)


def createFolder(folder):
    "create a folder"
    if not os.path.exists(folder): 
        os.makedirs(folder) 

def removeFolder(folder):
   "remove a folder and its content"
   if os.path.exists(folder):
      shutil.rmtree(folder)