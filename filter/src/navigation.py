import os
import time
import json
import glob
import pickle
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


def openBin(path):
    "open a binarie save"
    with open(path, 'rb') as file:
        bin = pickle.load(file)
    return bin


def writeBin(path,bin):
    "create a binarie save"
    with open(path, 'wb') as file:
        pickle.dump(bin, file)

