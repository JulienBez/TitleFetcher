import time

from src.navigation import *
from src.languages import *
from src.clustering import *

if __name__ == "__main__":

    start = time.time()

    #languageStep()
    test2()

    end = time.time()
    print(f"executed in {round(end - start,2)}")