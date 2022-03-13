import markovify
import pandas as pd
import re
import argparse
import json
import nltk
from nltk.tokenize import word_tokenize



class MyText(markovify.Text):

    def sentence_split(self, text):
        return re.split(r"\s*\n\s*", text)

    def word_join(self, words):
        return " ".join(reversed(words))


# разделяет стих на отдельные строки
def preprocess(line):
    if not line:
        return " "
    new = []
    lines = str(line).split('\n')
    for line in lines:
        new.extend(['\n']+[word.lower() for word in word_tokenize(str(line)) if word.isalpha()])
    return " ".join(reversed(new))


def main(args):
    models = []
    for file in args.input_files:
        # подготовка и очистка данных
        data = pd.read_csv(file, header=None, usecols=[4])
        data['clean_reversed'] = data[4].apply(preprocess)
        text = " \n ".join(map(str, list(data['clean_reversed'])))

        # обучение модели
        text_model = MyText(text, state_size=2, retain_original=False)

        # объединение моделей
        models.append(text_model)

    combined_model = markovify.combine(models)
    model_json = combined_model.to_json()
    with open(args.output_file, 'w') as f:
        json.dump(model_json, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-files", nargs='+', required=True)
    parser.add_argument("-o", "--output-file", required=True)
    args = parser.parse_args()
    main(args)
