#!/bin/bash

echo "# MovieFinder #"
(cd MovieFinder && python3 movieMain.py)

echo "# PaperFinder #"
(cd PaperFinder && python3 paperMain.py)

echo "# PressFinder #"
(cd PressFinder && python3 pressMain.py)

echo "Done !"