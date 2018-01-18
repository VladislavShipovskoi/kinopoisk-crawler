# -*- coding: utf-8 -*-
import csv
import re
import string
from collections import Counter
import pandas as pd
import pymorphy2
import nltk
from nltk import word_tokenize
from nltk.util import ngrams


def processing_text(text_file,stopwords_file=None):

    list_of_words = list()
    list_of_reviews = list()


    with open(text_file) as csvfile:
        a=0
        readcsv = csv.reader(csvfile, delimiter=',')
        for row in readcsv:
            a+=1
            row = row[0]
            list_of_reviews.append(row)
        print(a)

    for text in list_of_reviews:
        # text = re.sub(r'(?:(?:\d+,?)+(?:\.?\d+)?)', '', text)
        # text = re.sub(r'[^a-zA-Zа-яеёА-ЯЕЁ0-9-_*.]', ' ', text)
        # text = text.lower()
        # text = re.sub(r'\s+', ' ', text)
        # text = ' '.join(word.strip(string.punctuation) for word in text.split())
        # text = text.replace(' не ', ' не_')
        # text = ' '.join(word for word in text.split() if len(word) > 1)
        separated_sentence = re.sub("[^\w]", " ", text).split()
        list_of_words.append(separated_sentence)

    flat_list = [item for sublist in list_of_words for item in sublist]

    list_after_pos_tagging = list()
    morph = pymorphy2.MorphAnalyzer()

    for word in flat_list:
        p = morph.parse(word)[0]
        if p.tag.POS in['NOUN','ADJF','ADJS','ADVB']:
            word = p.normal_form
            # word = str(p.tag.POS)+'_'+word
            list_after_pos_tagging.append(word)

    bigrams = ngrams(list_after_pos_tagging, 2)
    # print(bigrams)

    word_frequency = Counter(bigrams)
    word_frequency = {k: v for k, v in word_frequency.items() if v > 100}
    word_frequency = sorted(word_frequency.items(), key=lambda item: (-item[1], item[0]))

    df = pd.DataFrame(word_frequency, columns=["word","frequence"])
    df.to_csv('../../data/negative_bigrams', index=False)


def main():
    # stopwords_file = '../../data/kinopoisk_review/negative'
    processing_text('../../data/kinopoisk_review/negative.csv')


if __name__ == "__main__":
    main()