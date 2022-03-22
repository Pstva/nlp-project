import argparse
import pandas as pd
import json
import torch
import numpy as np
from tqdm import tqdm
from collections import Counter, defaultdict
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset, TensorDataset


class PoetryLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_layers, device, dropout=0.15):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.vocab_size = vocab_size
        self.device=device

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_size, num_layers=num_layers, dropout=dropout,
                            batch_first=True)
        self.fc1 = nn.Linear(hidden_size, vocab_size)

    def forward(self, X, h=None, c=None):
        if h is None:
            h, c = self.init_state(X.size(0))
        out = self.embedding(X)
        out, (h, c) = self.lstm(out, (h, c))
        out = out.contiguous().view(-1, self.hidden_size)
        out = self.fc1(out)
        out = out.view(-1, X.size(1), self.vocab_size)
        out = out[:, -1]

        return out, h, c

    def init_state(self, batch_size):
        num_l = self.num_layers
        hidden = torch.zeros(num_l, batch_size, self.hidden_size).to(self.device)
        cell = torch.zeros(num_l, batch_size, self.hidden_size).to(self.device)
        return hidden, cell


def get_vocab(sentences):
    s = set()
    for sentence in sentences:
        s.update(sentence.split())

    vocab = defaultdict(lambda: 0)
    vocabr = defaultdict(lambda: "<unk>")
    vocab["<unk>"] = 0
    vocabr[0] = "<unk>"
    vocab["<pad>"] = 1
    vocabr[1] = "<pad>"
    idx = 2

    for word in s:
        vocab[word] = idx
        vocabr[idx] = word
        idx += 1
    return vocab, vocabr


def tokenize(sentences, vocab, max_length=10):
    data = list()
    for sentence in sentences:
        token_list = [vocab[word] for word in sentence.split()]
        for i in range(1, len(token_list)):
            b = max(0, i-max_length)
            n_gram_seq = torch.tensor(token_list[b:i+1], dtype=torch.long)
            data.append(n_gram_seq)
    return data


def generate_print_poem(model, vocab, vocabr, DEVICE, MAX_LENGTH, seed_text='кота'):
    model.eval()

    next_words = 20

    for i in range(next_words):
        token_list = np.ones(10, dtype=int)
        text_token = np.array([vocab[word] for word in seed_text.split(" ")][-MAX_LENGTH:])

        token_list[:len(text_token)] = text_token
        token_list = torch.from_numpy(token_list).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            out, h, c = model(token_list)

        idx = int(torch.argmax(out))
        new_word = vocabr[idx]  # if idx in vocabr else "<unk>"
        seed_text += " " + new_word

    for i, word in enumerate(reversed(seed_text.split())):
        print(word, end=" "),
        if i != 0 and (i + 1) % 5 == 0:
            print("\n")


def save_model(epoch, model, optimizer, loss, PATH):
    torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, PATH)


def train_model(vocab, EPOCHS, train_dataloader, DEVICE, output_path):

    VOCAB_SIZE = len(vocab)
    EMBEDDING_DIM = 128
    HIDDEN_SIZE = 512
    NUM_LAYERS = 3

    model = PoetryLSTM(VOCAB_SIZE, EMBEDDING_DIM, HIDDEN_SIZE, NUM_LAYERS, DEVICE).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    model.train()

    for epoch in tqdm(range(EPOCHS)):
        epoch_loss = 0
        for X, y in tqdm(train_dataloader):
            model.train()
            X = X.to(DEVICE)
            y = y.to(DEVICE)

            optimizer.zero_grad()
            output, h, c = model(X)
            loss = criterion(output, y)
            epoch_loss += loss.item()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 5)
            optimizer.step()

        #generate_print_poem(model, seed_text='я тебя любил')

        if (epoch + 1) % 5 == 0:
            save_model(epoch, model, optimizer, loss, f"{output_path}{epoch + 1}ep_128x512x3_bypoem.pth")

        print(f"Epoch: {epoch + 1} Loss:{epoch_loss / len(train_dataloader)}")



def main(args):
    print('preparing data...')
    MAX_LENGTH = int(args.max_length)
    df_sentences = pd.read_csv(args.input_data, header=None)
    vocab, vocabr = get_vocab(df_sentences[0])
    train_data = tokenize(df_sentences[0], vocab, max_length=MAX_LENGTH)

    # сохранение словаря для генерации стихов после обучения
    with open(args.vocab_path, 'w') as f:
        json.dump(vocab, f)

    X_train = [i[:-1] for i in train_data]  # taking all the words except the last in the input set
    y_train = [i[-1] for i in train_data]

    X_train = pad_sequence(X_train, batch_first=True, padding_value=vocab['<pad>'])
    y_train = torch.from_numpy(np.array(y_train))

    train_data = TensorDataset(X_train, y_train)

    BATCH_SIZE = int(args.batch_size)
    train_dataloader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)

    DEVICE = args.device

    print('starting training..')
    train_model(vocab, int(args.epochs), train_dataloader, DEVICE, args.output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-data", required=True)
    parser.add_argument("-v", "--vocab-path", required=True)
    parser.add_argument("-d", "--device", default='cpu')
    parser.add_argument("-b", "--batch-size", default=100)
    parser.add_argument("-m", "--max-length", default=10)
    parser.add_argument("-e", "--epochs", default=50)
    parser.add_argument("-o", "--output-path", required=True)
    args = parser.parse_args()
    main(args)
