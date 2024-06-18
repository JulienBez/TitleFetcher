import time

from src.navigation import *
from src.languages import *

if __name__ == "__main__":

    start = time.time()

    languageStep()

    end = time.time()
    print(f"executed in {round(end - start,2)}")