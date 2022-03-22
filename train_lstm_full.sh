#!/bin/sh


#было обучено на Kaggle

!python3 src/train_lstm.py -i data/full_data_clean_reversed.csv -o models/lstms/ -e 60 -v models/lstms/lstm_vocab.json -d "cuda" -b 512
