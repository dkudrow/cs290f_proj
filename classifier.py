from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.probability import FreqDist
import random

#Gather all tagged sentences into a single collection
#dir: directory 
#TAGS: POS, NEG
def getSentenceTagCollection(dir):
	fileList = os.listdir(dir)
	tagSentences = []	
	for file in fileList:
		f = open(dir + "/" + file)
		raw = f.read()
		sentences = sent_tokenize(raw)
		fileState = file.split("_")[1]		# pos OR neg
				
		if(fileState ==  "pos"):
			tagSentences += [(sent, 'POS') for sent in sentences]					
		else:
			tagSentences += [(sent, 'NEG') for sent in sentences]

	random.shuffle(tagSentences)
	return tagSentences


#Get Features for a given sentence
#Feature: [use, share] - counts
def getFeatures(sentence):
	features = [0, 0]
	tokens = word_tokenize(sentence)
	for token in tokens:
		if token == "use" or token == "using" or \
		   token == "uses" or token == "used":
			features[0] +=1
		elif token == "share" or token == "shares" or \
		     token == "sharing" or token == "shared":
			features[1] +=1
	return features
			

def main():
	tagSentences = getSentenceTagCollection("corpus_2")
	featureSet = [(getFeatures(sentence), tag) for (sentence, tag) in tagSentences]
	trainSet, testSet = featureSet[60:], featureSet[:36]
	print featureSet
	classifier = nltk.NaiveBayesClassifier.train(trainSet)	
main()


#print getFeatures("use share using shares share")
#print len(getSentenceTagCollection("corpus_2"))

#neg_file = open("corpus_2/google_neg")
#neg_raw = neg_file.read()

#print neg_raw
