import json
import pandas as pd
import random
import argparse
from russian_g2p.russian_g2p.Accentor import Accentor
from nltk.tokenize import word_tokenize
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

class RhymeSearch:
    """
    with_accent=False
        Составляет словарь по текстам вида
        'окончание (2-3 символа)': [список слов с таким окончанием]
    with_accent=True
        словарь с окончаниями с ударениями
    """

    def __init__(self, with_accent=False):
        self.rhymes_dict = {}
        self.with_accent = with_accent

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
        if self.with_accent:
            acc = Accentor(use_wiki=False)

        for word in tqdm(texts):
            if self.with_accent:
                # слово с ударением
                word_with_acc = acc.do_accents([[word]])[0][0]
                # индекс ударения
                acc_ind = word_with_acc.find("+")

            # если ищем без ударений или ударение не проставлено
            if not self.with_accent or acc_ind == -1:
                # то просто берем окончания по последним 2-3 буквам
                w1 = word.lower().strip()[-3::]
                w2 = word.lower().strip()[-2::]

            # иначе добавляем окончания с ударениями
            else:
                # начиная от буквы до ударной гласной
                w1 = word_with_acc[acc_ind-2:]
                # начиная от ударной гласной
                w2 = word_with_acc[acc_ind-1:]

            # добавляем окончания в словарь
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

        если self.with_accent=True, то сначала ищет с ударениями -
        окончание с буквы до ударной, затем с окончанием с ударной буквы, и потом без ударения
        """
        # просто окончания слова, без ударения
        w1 = word.lower().strip()[-3::]
        w2 = word.lower().strip()[-2::]

        # достаем окончания с ударением
        if self.with_accent:
            acc = Accentor(use_wiki=False)
            word_with_acc = acc.do_accents([[word]])[0][0]
            acc_ind = word_with_acc.find("+")
            w1_acc = word_with_acc[acc_ind - 2:]
            w2_acc = word_with_acc[acc_ind - 1:]

        # сначала пытаемся найти рифму по ударению

        if self.with_accent:
            rh = list(set(self.rhymes_dict[w1_acc]))
            # если нет рифмующихся слов на первый вид окончания с ударением, переходим ко второму
            if w1_acc not in self.rhymes_dict or len(rh) == 1:
                w1_acc = w2_acc
            if w1_acc in self.rhymes_dict and len(rh) > 1:
                # пытаемся 10 раз найти рифму
                j = 0
                while j < 10:
                    choice_ind = random.randint(0, len(rh) - 1)
                    if rh[choice_ind] != word:
                        return rh[choice_ind]
                    j += 1

        rh = list(set(self.rhymes_dict[w1]))
        # если не вышло или поиск был без ударения, то ищем по окончаниям
        if w1 not in self.rhymes_dict or len(rh) == 1:
            w1 = w2

        if w1 in self.rhymes_dict and len(rh) > 1:
            # пытаемся 10 раз найти рифму
            j = 0
            while j < 10:
                choice_ind = random.randint(0, len(rh) - 1)
                if rh[choice_ind] != word:
                    return rh[choice_ind]
                j += 1

        # если рифма не найдена, вернет None


# выдает слова из текстов стихов по одному
def words_generator(texts):
    words = set()
    for text in texts:
        lines = str(text).split('\n')
        for line in lines:
            tokenized = [word.lower() for word in word_tokenize(str(line)) if word.isalpha()]
            for word in tokenized:
                if word not in words:
                    words.add(word)
                    yield word


def main(args):
    data = pd.read_csv(args.input_file, usecols=[4], header=None)
    texts = data[4]
    rhyme_search = RhymeSearch(with_accent=args.accent)
    words = words_generator(texts)
    rhyme_search.train(words)
    rhyme_search.save_json(args.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-o", "--output-file", required=True)
    parser.add_argument("-a", "--accent", required=False, default=False)
    args = parser.parse_args()
    main(args)
