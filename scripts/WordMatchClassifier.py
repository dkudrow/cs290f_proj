import os
import random 

from nltk import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

wordList = ["use", "share"]

def getTagged(dir):
    fileList = os.listdir(dir)
    tagged = []
    for file in fileList:
        f = open(dir + "/" + file)
        raw = f.read()
        sentences = sent_tokenize(raw)
        tag = file.split("_")[1]
        if (tag == "pos"):
            tagged += [(sent, 'POS') for sent in sentences]
        else:
            tagged += [(sent, 'NEG') for sent in sentences]

        random.shuffle(tagged)

    return tagged

def getFeatures(sentence):
    features = {}
    for word in wordList:
        features[word] = False

    tokens = word_tokenize(sentence)

    for token in tokens:
        for word in wordList:
            if word.find(stemmer.stem(token)) >= 0:
                features[word] = True
                break

    return features
