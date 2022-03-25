import markovify
import json
import argparse
import csv
from train_markov import MyText
from search_rhyme import RhymeSearch


class Stihi:
    def __init__(self, model, rhyme_model):
        self.model = model
        self.rhyme_model = rhyme_model

    def generate_stih(self, lines_n=4, rhyme_scheme='0101'):

        assert lines_n == len(rhyme_scheme)
        lines, rhyme_words = [], []

        # подсчет для каждой строки индекс рифмованной строки
        pred_rhyme, last_rh_ind = [], {}
        for i, rh in enumerate(rhyme_scheme):
            if rh not in last_rh_ind:
                last_rh_ind[rh] = i
                pred_rhyme.append(-1)
                continue
            pred_rhyme.append(last_rh_ind[rh])
            last_rh_ind[rh] = i

        # генерация строк
        for i in range(lines_n):
            # последняя строка, с которой надо рифмоваться
            last_rhyme_line = pred_rhyme[i]
            end = None
            if last_rhyme_line != -1:
                end = rhyme_words[pred_rhyme[i]]
            # сгенерированная линия
            res = self.generate_line(end_word=end)
            if res is None:
                return None

            cur_text, rhyme_word = res
            lines.append(cur_text)
            rhyme_words.append(rhyme_word)
        return lines

    def generate_line(self, end_word=None, n_try=10):

        # n_try раз пытается сгенерировать строку
        for i in range(n_try):
            # с заданным последним словом
            if end_word:
                second_rhyme = self.rhyme_model.give_rhyme(end_word)

                # для слова нет рифмы
                if not second_rhyme:
                    return None
                # тут модуль часто выдает ошибку ParamError,
                # что не может сгенерить с таким словом
                try:
                    cur_text = self.model.make_sentence_with_start(second_rhyme, strict=False,
                                                                   min_words=3, max_words=8)
                except:
                    continue

            # рандомное предложение
            else:
                cur_text = self.model.make_sentence(min_words=3, max_words=8)

            if cur_text and cur_text.split()[-1] != 'nan':
                # последнее слово
                second_rhyme = cur_text.split()[-1]
                return cur_text, second_rhyme

        # не нашли строку
        return None


def main(args):
    # загрузка одной или нескольких марковских моделей
    if len(args.markov_models) > 1:
        models = []
        for model_path in args.markov_models:
            with open(model_path, 'r') as f:
                model_json = json.load(f)
                models.append(MyText.from_json(model_json))

        text_model = markovify.combine(models)
    else:
        with open(args.markov_models[0], 'r') as f:
            model_json = json.load(f)
        text_model = MyText.from_json(model_json)
    text_model.compile(inplace=True)

    # загрузка одной или нескольких модели для рифмы
    rhyme_model = RhymeSearch(with_accent=args.accent)
    rhyme_model.from_json(args.rhyme_models[0])
    for rhyme_path in args.rhyme_models[1:]:
        new_rhyme = RhymeSearch()
        new_rhyme.from_json(rhyme_path)
        rhyme_model.merge_models(new_rhyme)

    # генерация стихов
    stihi = []
    stih_generator = Stihi(text_model, rhyme_model)
    while len(stihi) < int(args.number_generate):
        s = stih_generator.generate_stih(lines_n=args.lines_generate, rhyme_scheme=args.rhyme_scheme)
        if s:
            stihi.append(" \n ".join(s))

    if args.output_file is None:
        for stih in stihi:
            print(stih)
            print()
    else:
        with open(args.output_file, 'w') as f:
            csvwriter = csv.writer(f, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for ind, stih in enumerate(stihi):
                csvwriter.writerow([ind, stih])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--markov-models", nargs='+', required=True)
    parser.add_argument("-r", "--rhyme-models", nargs='+', required=True)
    parser.add_argument("-n", "--number-generate",  required=False, default=5)
    parser.add_argument("-l", "--lines-generate",  required=False, default=4)
    parser.add_argument("-s", "--rhyme-scheme",  required=False, default='0101')
    parser.add_argument("-o", "--output-file",  required=False, default=None)
    parser.add_argument("-a", "--accent", required=False, default=False)
    args = parser.parse_args()
    main(args)