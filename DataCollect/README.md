# DataCollect

In order to create our corpus, we searched for titles in 3 main sources : movies, press and scientific papers. This folder contains every scripts we used to collect those titles.

## MovieFinder

This is a very simple script that allows us to download, read and extract titles from [IMDb non-commercial datasets](https://developer.imdb.com/non-commercial-datasets/). Since those datasets are said to be updated daily, the number of collected titles may vary. To use it :

```
python MovieFinder/movieMain.py
```

The resulting dataset (dict_movies.json) will be stored in the newly created **MovieFinder/data** folder. This script collects around 10 million movie titles.

## PaperFinder

This script allows us to fetch scientific article titles from the [OpenAlex](https://openalex.org/) website. We use [OpenAlex' API](https://docs.openalex.org/how-to-use-the-api/api-overview) in order to do so. To use it :

```
python PaperFinder/paperMain.py
```

**Warning** : this script fetch around 14 million scientific paper titles, which might take a while. We managed to fetch 1 million titles / hour while running 4 parallel instances of this script, but this might not be an ideal solution. Use with caution. Finally, run you have to run the following script :

```
python PaperFinder/metadata.py
```

The resulting dataset (around 70 json files) will be stored in the newly created **PaperFinder/data/merge** folder. 

## PressFinder

We search for press article titles from (Felix Leeb & Bernhard Schölkopf, 2024) corpus, Babel Briefings. Since it is needed to be logged in either to [Kaggle](https://www.kaggle.com/datasets/felixludos/babel-briefings) or [HuggingFace](https://huggingface.co/datasets/felixludos/babel-briefings) in order to download this corpus, it must be downloaded manually and then extracted in **PressFinder/data** folder. Once it is done, you can simply run :

```
python PressFinder/pressMain.py
```

The resulting dataset (dict_press.json) will be stored in the **PressFinder/data** folder. This script collects around 4 million press article titles.
