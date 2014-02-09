# 
# util.py -- some helper functions to speed things up
# 

import nltk

def buildCorpus():
    return nltk.corpus.PlaintextCorpusReader("data/text/", ".*")

