import json
import pandas as pd
import random
import argparse
import nltk
from nltk.tokenize import word_tokenize


class RhymeSearch:
    """
    Составляет словарь по текстам вида
    'окончание (2-3 символа)': [список слов с таким окончанием]
    """

    def __init__(self):
        self.rhymes_dict = {}

    def from_json(self, path):
        with open(path, 'r') as f:
            self.rhymes_dict = json.load(f)

    def save_json(self, path):
        with open(path, 'w') as f:
            json.dump(self.rhymes_dict, f)

    def merge_models(self, new_model):
        """
        к текущему словарю добавляет значения другой модели
        """
        for k, v in new_model.rhymes_dict.items():
            if k in self.rhymes_dict:
                self.rhymes_dict[k].extend(v)
            else:
                self.rhymes_dict[k] = v


    def train(self, texts):
        """
        texts - list со словами или генератор их выдающий
        слово добавляется в рифму по его последним 2 и 3 буквам
        """
        for word in texts:
            w1 = word.lower().strip()[-3::]
            w2 = word.lower().strip()[-2::]
            if w1 in self.rhymes_dict:
                self.rhymes_dict[w1].add(word)
            else:
                self.rhymes_dict[w1] = {word}

            if w2 in self.rhymes_dict:
                self.rhymes_dict[w2].add(word)
            else:
                self.rhymes_dict[w2] = {word}

        for k, v in self.rhymes_dict.items():
            self.rhymes_dict[k] = list(v)

    def give_rhyme(self, word):
        """
        выдает рифму - слово, имеющее то же окончание (2 или 3 буквы)
        если есть с 3, то выдает для него, иначе для 2 букв
        """
        w1 = word.lower().strip()[-3::]
        w2 = word.lower().strip()[-2::]

        if w1 not in self.rhymes_dict or len(self.rhymes_dict[w1]) > 1:
            w1 = w2

        if w1 in self.rhymes_dict and len(self.rhymes_dict[w1]) > 1:
            while True:
                rh = self.rhymes_dict[w1]
                choice_ind = random.randint(0, len(rh) - 1)
                if rh[choice_ind] != word:
                    return rh[choice_ind]


# выдает слова из текстов стихов по одному
def words_generator(texts):
    for text in texts:
        lines = str(text).split('\n')
        for line in lines:
            tokenized = [word.lower() for word in word_tokenize(str(line)) if word.isalpha()]
            yield from tokenized


def main(args):
    data = pd.read_csv(args.input_file, usecols=[4], header=None)
    texts = data[4]
    rhyme_search = RhymeSearch()
    words = words_generator(texts)
    rhyme_search.train(words)
    rhyme_search.save_json(args.output_file)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-o", "--output-file", required=True)
    args = parser.parse_args()
    main(args)
