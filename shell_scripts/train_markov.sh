#!/bin/sh

# модели по категориям
python3 src/train_markov.py  -i data/poems_2020_civil.csv data/poems_2021_civil.csv -o models/markov/civil.json
python3 src/train_markov.py  -i data/poems_2020_love.csv data/poems_2021_love.csv -o models/markov/love.json
python3 src/train_markov.py  -i data/poems_2020_nature.csv data/poems_2021_nature.csv -o models/markov/nature.json
python3 src/train_markov.py  -i data/poems_2020_religion.csv data/poems_2021_religion.csv -o models/markov/religion.json
