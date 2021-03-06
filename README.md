# nlp-project

### Структура репозитория

#### Данные
[Код для парсинга данных](src/parser_links_stihi.py).

[Команда для запуска скрипта](shell_scripts/parse_2000_2022.sh)

Данные со стихами за 2020-2021 гг лежат в папке [data](data/).

Спарсены все стихи за указанные года из 4 **категорий**:

+ Гражданская лирика (14 тема)
+ Любовная лирика (01 тема)
+ Пейзажная лирика (02 тема)
+ Религиозная лирика (19 тема)

#### Контроль рифмы
[Код для подсчета словарей рифма и подбора рифмы](src/search_rhyme.py)

[Команда для запуска скритпа](shell_scripts/make_rhyme_jsons.sh)

#### Марковские модели
[Код для обучения марковских моделей](src/train_markov.py)

[Код для генерации стихов марковскими моделями](src/generate_markov.py)

[Команды для обучения](shell_scripts/train_markov.sh)

[Команды для генерации](shell_scripts/make_markov_examples.sh)

#### LSTM
[Код для подготовки данных для lstm](src/prepare_data_lstm2.py)

[Код для обучения lstm](src/train_lstm.py)

[Код для обучения lstm с предобученными эмбеддингами](src/train_lstm_with_pretrained_emb.py)

[Команды для обучения](shell_scripts/train_lstm_full.sh)

[Код для генерации стихотворений с помощью lstm](generate_lstm_poems.ipynb)

#### Оценка генерации
[Оценка генерации предобученной моделью ruGPT2](LM_evaluation.ipynb)

[Подсчет статистик для оценок](LM_evaluation_stats.ipynb)

#### Примеры генерации
[Сгенерированные стихи](generated_poems/)

[Сгенерированные стихи с оценкой gpt](generated_poems/with_lp/)

#### Модели
Все модели доступны по [ссылке](https://drive.google.com/drive/folders/1bX_k1bVUJYpp_0_jouH5CoSNSMgPLxc9?usp=sharing)



### Описание данных:
+ Ссылка на стих
+ Имя автора
+ Ссылка на автора
+ Название стиха
+ Текст стиха

Всего произведений в изначальных данных:

+ poems_2020_civil.csv - **13532**
+ poems_2021_civil.csv - **14633**
+ poems_2020_love.csv - **13876**
+ poems_2021_love.csv - **14756**
+ poems_2020_nature.csv - **12161**
+ poems_2021_nature.csv - **12443**
+ poems_2020_religion.csv - **12225**
+ poems_2021_religion.csv - **13112**


