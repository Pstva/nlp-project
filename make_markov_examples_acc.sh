#!/bin/sh

python3 src/generate_markov.py  -m models/markov/civil.json -r data/rhymes_acc_2020_civil.json  data/rhymes_acc_2021_civil.json -n 90 -o generated_poems/markov_acc_civil.csv -a True
python3 src/generate_markov.py  -m models/markov/love.json -r data/rhymes_acc_2020_love.json  data/rhymes_acc_2021_love.json -n 90 -o generated_poems/markov_acc_love.csv -a True
python3 src/generate_markov.py  -m models/markov/nature.json -r data/rhymes_acc_2020_nature.json  data/rhymes_acc_2021_nature.json -n 90 -o generated_poems/markov_acc_nature.csv -a True
python3 src/generate_markov.py  -m models/markov/religion.json -r data/rhymes_acc_2020_religion.json  data/rhymes_acc_2021_religion.json -n 90 -o generated_poems/markov_acc_religion.csv -a True
