from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.probability import FreqDist

#Create a corpus
corpusdir = "corpus/"
newcorpus = PlaintextCorpusReader(corpusdir, '.*')
corpusWords = nltk.Text(newcorpus.words())
posTags = nltk.pos_tag(corpusWords)


#Total number of words in corpus
def getTotalNumberOfWords(words):
	return len(words)

#Number of unique words in corpus
def getNumberOfUniqueWords(words):
	return len(set(words))

#Most frequently used 25 words
def getMostFreqWords(words):
	fdist = FreqDist(words)
	vocab = fdist.keys()
	return vocab[:25]


#Name List
def getNameList(tags):
	nameList = []
        for (word, tag) in tags:
                if tag == "NN" or tag == "NNP" or tag == "NNS":
                	#if tag == "NN":        
			nameList.append(word)
	return nameList

#Number of Names - occurrences
def getNumberOfNames(nameList):
	return len(nameList)

#Most frequently used 25 names
def getMostFreqNames(nameList):
	nameDist = FreqDist(nltk.Text(nameList))
	nameVocab = nameDist.keys()
	return nameVocab[:25]

#Verb List
def getVerbList(tags):
	verbList = []
        for (word, tag) in tags:
                if tag == "VB" or tag == "VBP" or tag == "VBN" \
                   or tag == "VBD" or tag == "VBG":
                        verbList.append(word)
	return verbList

#Number of Verbs - occurrences
def getNumberOfVerbs(verbList):
	return len(verbList)

	
#Most frequently used 25 verbs
def getMostFreqVerbs(verbList):
        verbDist = FreqDist(nltk.Text(verbList))
        verbVocab = verbDist.keys()
        return verbVocab[:25]


#Files in the corpus
def getFileIDs(corpus):
	return corpus.fileids()






#print getFileIDs(newcorpus)
#nameList = getNameList(posTags)
#print getNumberOfNames(nameList)
#print getMostFreqNames(nameList)


#verbList = getVerbList(posTags)
#print getNumberOfVerbs(verbList)
#print getMostFreqVerbs(verbList)


#print "Total Words: %i" % getTotalNumberOfWords(corpusWords)
#print "Unique Words: %i" % getNumberOfUniqueWords(corpusWords)
#print getMostFreqVerbs(posTags)	
#print getMostFreqNames(posTags)
#print getMostFreqWords(newcorpus) 



#################################################################################################

#mytext = nltk.Text(newcorpus.words())
#mytext.dispersion_plot(["use", "we", "you", "collect", "personal", "party", "email", "contact"])

#text = newcorpus.words()
#text1 = nltk.word_tokenize("They race each other")
#text2 = nltk.word_tokenize("A harsh race")
#tags1 = nltk.pos_tag(text1)
#tags2 = nltk.pos_tag(text2)
#print tags1
#print "--------"
#print tags2


#tagged_token = nltk.tag.str2tuple('fly/ERD')
#print tagged_token



#for word in words:
#	print word



#for infile in sorted(newcorpus.fileids()):
#	print infile
#	with newcorpus.open(infile) as fin:
#		print fin.read().strip()
