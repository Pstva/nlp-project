#!/bin/sh
# без ударения
python3 src/search_rhyme.py  -i data/poems_2020_civil.csv -o data/rhymes_2020_civil.json
python3 src/search_rhyme.py -i data/poems_2021_civil.csv -o data/rhymes_2021_civil.json

python3 src/search_rhyme.py  -i data/poems_2020_love.csv -o data/rhymes_2020_love.json
python3 src/search_rhyme.py -i data/poems_2021_love.csv -o data/rhymes_2021_love.json

python3 src/search_rhyme.py -i data/poems_2020_nature.csv -o data/rhymes_2020_nature.json
python3 src/search_rhyme.py -i data/poems_2021_nature.csv -o data/rhymes_2021_nature.json

python3 src/search_rhyme.py -i data/poems_2020_religion.csv -o data/rhymes_2020_religion.json
python3 src/search_rhyme.py -i data/poems_2021_religion.csv -o data/rhymes_2021_religion.json

# с ударением
python3 src/search_rhyme.py  -i data/poems_2020_civil.csv -o data/rhymes_acc_2020_civil.json -a True
python3 src/search_rhyme.py -i data/poems_2021_civil.csv -o data/rhymes_acc_2021_civil.json -a True

python3 src/search_rhyme.py  -i data/poems_2020_love.csv -o data/rhymes_acc_2020_love.json -a True
python3 src/search_rhyme.py -i data/poems_2021_love.csv -o data/rhymes_acc_2021_love.json -a True

python3 src/search_rhyme.py -i data/poems_2020_nature.csv -o data/rhymes_acc_2020_nature.json -a True
python3 src/search_rhyme.py -i data/poems_2021_nature.csv -o data/rhymes_acc_2021_nature.json -a True

python3 src/search_rhyme.py -i data/poems_2020_religion.csv -o data/rhymes_acc_2020_religion.json -a True
python3 src/search_rhyme.py -i data/poems_2021_religion.csv -o data/rhymes_acc_2021_religion.json -a True