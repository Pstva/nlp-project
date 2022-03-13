#!/bin/sh

python3 src/search_rhyme.py  -i data/poems_2020_civil.csv -o data/rhymes_2020_civil.json
python3 src/search_rhyme.py -i data/poems_2021_civil.csv -o data/rhymes_2021_civil.json

python3 src/search_rhyme.py  -i data/poems_2020_love.csv -o data/rhymes_2020_love.json
python3 src/search_rhyme.py -i data/poems_2021_love.csv -o data/rhymes_2021_love.json

python3 src/search_rhyme.py -i data/poems_2020_nature.csv -o data/rhymes_2020_nature.json
python3 src/search_rhyme.py -i data/poems_2021_nature.csv -o data/rhymes_2021_nature.json

python3 src/search_rhyme.py -i data/poems_2020_religion.csv -o data/rhymes_2020_religion.json
python3 src/search_rhyme.py -i data/poems_2021_religion.csv -o data/rhymes_2021_religion.json