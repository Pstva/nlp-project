import pandas as pd
import nltk
from nltk.tokenize import word_tokenize


def preprocess(text):
    if not text:
        return ""
    new_text = []
    lines = str(text).split('\n')
    for line in lines:
        words = " ".join(reversed([word.lower() for word in word_tokenize(str(line)) if word.isalpha()]))
        if len(words) < 1:
            continue
        new_text.append(words)
    return " \n ".join(new_text)


def define_cat(name):
    if "civil" in name:
        return "civil"
    if "love" in name:
        return "love"
    if "nature" in name:
        return "nature"
    if "religion" in name:
        return "religion"


def main():
    data_files = ["poems_2021_civil.csv", "poems_2020_civil.csv", "poems_2021_love.csv", "poems_2021_nature.csv",
                  "poems_2020_love.csv", "poems_2021_religion.csv", "poems_2020_nature.csv", "poems_2020_religion.csv"]
    full_data = pd.DataFrame(columns=['poems', 'cat'])
    for data_file in data_files:
        d = pd.read_csv("data/"+data_file, header=None, usecols=[4])
        d['len_text'] = d[4].apply(lambda x: len(str(x)))
        # отрезаем стихи по длине
        d = d[d['len_text'].quantile(0.25) < d['len_text']][d['len_text'] < d['len_text'].quantile(0.75)]
        d.rename({4 : 'poems'}, axis=1, inplace=True)
        d['cat'] = define_cat(data_file)
        full_data = pd.concat([full_data, d[['poems', 'cat']]], axis=0)

    full_data['clean_reversed'] = full_data['poems'].apply(preprocess)
    full_data[['cat', 'clean_reversed']].to_csv('data/full_data_clean_reversed.csv', index=False)


if __name__ == "__main__":
    main()



