#!/bin/sh


#было обучено на Kaggle

!python3 src/train_lstm.py -i data/full_data_clean_reversed.csv -o models/lstms/ -e 60 -v models/lstms/lstm_vocab.json -d "cuda" -b 512

# с предобученнными эмбеддингами
!python3 src/train_lstm.py -i data/full_data_clean_reversed.csv -o models/lstms/ -e 60 -v models/lstms/lstm_vocab.json -d "cuda" -b 512

!wget https://storage.yandexcloud.net/natasha-navec/packs/n..
!python3 src/train_lstm_with_pretrained_emb.py -i data/full_data_clean_reversed.csv -e 60 -b 400 -o models/lstms/ -e 60 -v models/lstms/lstm_vocab_emb.json -d "cuda" -n "navec_hudlit_v1_12B_500K_300d_100q.tar"
