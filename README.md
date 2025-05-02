# TitleFetcher

With the aim to collect titles from different sources for later use, we searched for titles in 3 main sources : movies, press papers and scientific papers. This folder contains every scripts we used to collect those titles. You can execute everything at once using the following script:

```
bash executeAll.sh
```

**However**, before executing this script, be aware 1) that you need to download and extract in **PressFinder/data** the [Babel Briefings](https://www.kaggle.com/datasets/felixludos/babel-briefings) corpus (Felix Leeb & Bernhard Schölkopf, 2024) and 2) that the whole process might take up to 15 hours. 

If you wish to fetch titles from only one of the three sources availables, we introduce below each collect we proceeded to.

## MovieFinder

This is a very simple script that allows us to download, read and extract titles from [IMDb non-commercial datasets](https://developer.imdb.com/non-commercial-datasets/). Since those datasets are said to be updated daily, the number of collected titles may vary. To use it, go to **MovieFinder** folder and use the following command:

```
python movieMain.py
```

The resulting dataset will be stored in the newly created **MovieFinder/data/split** folder. This script collects around 12 million movie titles. Note that we remove a large number of irrevelant titles (like episodes numbers with no other informations) and try to determine the language of titles without referenced language.

## PaperFinder

This script allows us to fetch scientific article titles from the [OpenAlex](https://openalex.org/) website. We use [OpenAlex' API](https://docs.openalex.org/how-to-use-the-api/api-overview) in order to do so. To use it, go to **PaperFinder** folder and use the following command:

```
python paperMain.py
```

**Warning** : this script fetches around 14 million scientific paper titles, which might take a while. We managed to fetch 1 million titles / hour while running 4 parallel instances of this script, but this might not be an ideal solution. Use with caution. The resulting dataset will be stored in the newly created **PaperFinder/data/merge** folder. 

## PressFinder

We search for press article titles from (Felix Leeb & Bernhard Schölkopf, 2024) corpus, Babel Briefings. Since it is needed to be logged in either to [Kaggle](https://www.kaggle.com/datasets/felixludos/babel-briefings) or [HuggingFace](https://huggingface.co/datasets/felixludos/babel-briefings) in order to download this corpus, it must be downloaded manually and then extracted in **PressFinder/data** folder. Once it is done, you can simply go to **PressFinder** folder and use the following command:

```
python pressMain.py
```

The resulting dataset (dict_press.json) will be stored in the **PressFinder/data/split** folder. This script collects around 4 million press article titles.
