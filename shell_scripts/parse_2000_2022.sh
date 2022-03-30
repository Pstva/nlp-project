#!/bin/sh

# гражданская лирика, тема 14
python3 src/parser_links_stihi.py -y 2020 -t 14 -o data/poems_2020_civil.csv
python3 src/parser_links_stihi.py -y 2021 -t 14 -o data/poems_2021_civil.csv

# любовная лирика, тема 01
python3 src/parser_links_stihi.py -y 2020 -t 01 -o data/poems_2020_love.csv
python3 src/parser_links_stihi.py -y 2021 -t 01 -o data/poems_2021_love.csv

# пейзажная лирика, тема 02
python3 src/parser_links_stihi.py -y 2020 -t 02 -o data/poems_2020_nature.csv
python3 src/parser_links_stihi.py -y 2021 -t 02 -o data/poems_2021_nature.csv

# религиозная лирика, тема 19
python3 src/parser_links_stihi.py -y 2020 -t 19 -o data/poems_2020_religion.csv
python3 src/parser_links_stihi.py -y 2021 -t 19 -o data/poems_2021_religion.csv

