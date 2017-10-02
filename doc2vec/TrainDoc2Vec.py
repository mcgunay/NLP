#!/usr/bin/env python3
# -*- coding: iso-8859-9 -*-

import gensim
import pymongo
import os
from pymongo import MongoClient
from nltk import RegexpTokenizer
from pathlib import Path

def train_model(size, window, workers, min_count, alpha, epoch_count, reduce_alpha_by):
    #clean data
    def nlp_clean(data):
        new_data = []
        for d in data:
            new_str = d.lower()
            dlist = tokenizer.tokenize(new_str)
            dlist = list(set(dlist).difference(stopword_set))
            new_data.append(dlist)
        return new_data

    LabeledSentence = gensim.models.doc2vec.LabeledSentence

    class LabeledLineSentence(object):
        def __init__(self, doc_list, labels_list):
            self.labels_list = labels_list
            self.doc_list = doc_list

        def __iter__(self):
            for idx, doc in enumerate(self.doc_list):
                yield LabeledSentence(words=doc, tags=[self.labels_list[idx]])

    current_dir = os.path.abspath(os.path.dirname(__file__))
    #clean data with these words
    with open(current_dir+"/turkish.txt", encoding='iso-8859-9') as f:
        read_data = f.read().splitlines()

    tokenizer = RegexpTokenizer(r'\w+')
    stopword_set = read_data
    #connect to db to get the data
    client = MongoClient('mongodb://testuser:testuser@ds151014.mlab.com:51014/nlpdatabase')
    news = client.get_database("nlpdatabase").get_collection("news")

    datalabels = []
    data = []
    #little bit tidying up
    for post in news.find().sort("_id", pymongo.ASCENDING):
        datalabels.append(str(post["_id"]))
        data.append(post["text"])
    #clean data
    data = nlp_clean(data)

    it = LabeledLineSentence(data, datalabels)
    #train data according to parameters
    #model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate
    model = gensim.models.Doc2Vec(size=size, window=window, min_count=min_count, workers=workers,alpha=alpha, min_alpha=alpha) # use fixed learning rate
    model.build_vocab(it)
    for epoch in range(epoch_count):
        model.train(it, total_examples=len(data), epochs=model.iter)
        #model.alpha -= 0.002
        model.alpha -= reduce_alpha_by
        model.min_alpha = model.alpha
        model.train(it, total_examples=len(data), epochs=model.iter)
    #if model file exists remove old one
    my_file = Path(current_dir + "/doc2vec.bin")
    if my_file.exists():
        os.remove(my_file)
    #save the model
    model.save("doc2vec.bin")

