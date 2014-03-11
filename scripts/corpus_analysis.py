from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.probability import FreqDist

#Create a corpus
corpusdir = "/home/erdinc/nltk/cs290f_proj/tos/"
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
	return nameVocab[:50]

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
        return verbVocab[:50]


#Files in the corpus
def getFileIDs(corpus):
	return corpus.fileids()


#Write into file
def writeFile(fileName, list):
	file = open(fileName, 'w')
	for item in list:
		file.write("%s \n \n" % item)
	file.close()


#Get sentences in a corpus
def getSentences(dir):
	fileList = os.listdir(dir)
	sentences = []
	for file in fileList:
		f = open(dir + "/" + file)
		raw = f.read()
		sentences = sent_tokenize(raw)
		f.close()		

	return sentences


def getSignificantNouns():
	nounMap = {}
	nounMap['information'] 	= "N"
	nounMap['account'] 	= "N"
	nounMap['services'] 	= "N"
	nounMap['data'] 	= "N"
	nounMap['email'] 	= "N"
	nounMap['content'] 	= "N"
	nounMap['access'] 	= "N"
	nounMap['friends']	= "N"	
	nounMap['device'] 	= "N"
	nounMap['cookies'] 	= "N"
	nounMap['address'] 	= "N"
	nounMap['party'] 	= "N"
	nounMap['others'] 	= "N"
	nounMap['privacy']	= "N"
	nounMap['contact']	= "N"
	nounMap['name']		= "N"
	nounMap['location']	= "N"
	nounMap['settings']	= "N"
	nounMap['profile'] 	= "N"
	nounMap['user']		= "N"	
	nounMap['Data']		= "N"	
					
	return nounMap
	

def getSignificantVerbs():
	verbMap = {}
	verbMap['use'] 		= "V"
	verbMap['share'] 	= "V"
	verbMap['collect'] 	= "V"
	verbMap['shared'] 	= "V"
	verbMap['used'] 	= "V"
	verbMap['give'] 	= "V"
	verbMap['post'] 	= "V"
	verbMap['offer'] 	= "V"
	verbMap['disclose'] 	= "V"
	verbMap['store'] 	= "V"
	verbMap['delete']	= "V"
	verbMap['remove']	= "V"
	verbMap['uses']		= "V"

	return verbMap


def getSignificantAdj():
	adjMap = {}
	adjMap['public']	= "A"
	adjMap['Public']	= "A"

	return adjMap

def getCheapVerbs():
	cverbMap = {}
	cverbMap['improve'] 	= "C"
	#cverbMap['help'] 	= "C"
	cverbMap['protect'] 	= "C"
	cverbMap['provide']	= "C"

	return cverbMap

def getSentenceScore(sentence, nounMap, verbMap, adjMap, cverbMap):
	tokens = word_tokenize(sentence)
	noun_count = 0
	verb_count = 0	
	adj_count  = 0
	cverb_count = 0	

	for token in tokens:
		nounValue 	= nounMap.get(token, "nounError")
		verbValue 	= verbMap.get(token, "verbError")			
		adjValue 	= adjMap.get(token, "adjError")
		cverbValue 	= cverbMap.get(token, "cverbError")

		if nounValue == "N": 
			noun_count += 1

		if verbValue == "V":
			verb_count += 1
		
		if adjValue == "A":
			adj_count += 1		

		if cverbValue == "C":
			cverb_count += 1 	

	return checkCount(noun_count, verb_count, adj_count, 0, sentence, 6)
	
def checkCount(nounCount, verbCount, adjCount, cverbCount, sentence, significance):
	score = nounCount + 3*verbCount + 3*adjCount - cverbCount
	
	if score < significance:
		print "%s \t %i \n \n" % (sentence, score)
		return 1 		

	return 0


def getVerbDependencyScore(sentence, nounMap, verbMap, adjMap, cverbMap):
	tokens = word_tokenize(sentence)
	verbCoeff = 1
	noun_count = verb_count = adj_count = cverb_count = 0

	for token in tokens:
		nounValue       = nounMap.get(token, "nounError")
                verbValue       = verbMap.get(token, "verbError")
                adjValue        = adjMap.get(token, "adjError")
                cverbValue      = cverbMap.get(token, "cverbError")
		
		if nounValue == "N":
                        noun_count += verbCoeff

                if verbValue == "V":
                        verb_count += 1
			verbCoeff = 1

                if adjValue == "A":
                        adj_count += 1

                if cverbValue == "C":
                        cverb_count += 1
			verbCoeff = 0
		
	return checkCount(noun_count, verb_count, adj_count, cverb_count, sentence, 5)


def getSubjectDependencyScore(sentence, nounMap, verbMap, adjMap, cverbMap):
	tokens = word_tokenize(sentence)
	noun_count=verb_count=adj_count=cverb_count=0
	subjectCoeff=1
	verbCoeff=1

	for token in tokens:
                nounValue       = nounMap.get(token, "nounError")
                verbValue       = verbMap.get(token, "verbError")
                adjValue        = adjMap.get(token, "adjError")
                cverbValue      = cverbMap.get(token, "cverbError")
		
		if token == "We" or token == "we":
			subjectCoeff=1
			verbCoeff=1
		elif token == "You" or token == "you":
			subjectCoeff=0
			verbCoeff=0

                if nounValue == "N":
                        noun_count += verbCoeff

                if verbValue == "V":
                        verb_count += subjectCoeff

                if adjValue == "A":
                        adj_count += 1

                if cverbValue == "C":
                        cverb_count += 1
                        verbCoeff = 0

	return checkCount(noun_count, verb_count, adj_count, cverb_count, sentence, 5)




def globalSignificantTerms():
	nounMap = getSignificantNouns()
        verbMap = getSignificantVerbs()
        adjMap  = getSignificantAdj()
	cverbMap = getCheapVerbs()

        sentences = getSentences("/home/erdinc/nltk/cs290f_proj/tos_test/")

        high_sent_count = 0
        for sent in sentences:
                if getSentenceScore(sent, nounMap, verbMap, adjMap, cverbMap) == 1:
                        high_sent_count += 1

        print "Number of Sentences: %i " % len(sentences)
        print "Qualified Sentences: %i " % high_sent_count


def verbDependency():
	nounMap  = getSignificantNouns()
        verbMap  = getSignificantVerbs()
        adjMap   = getSignificantAdj()
        cverbMap = getCheapVerbs()

	sentences = getSentences("/home/erdinc/nltk/cs290f_proj/tos_test/")

	high_sent_count = 0
        for sent in sentences:
                if getVerbDependencyScore(sent, nounMap, verbMap, adjMap, cverbMap) == 1:
                        high_sent_count += 1

        print "Number of Sentences: %i " % len(sentences)
        print "Qualified Sentences: %i " % high_sent_count
			

def subjectDependency():
	nounMap = getSignificantNouns()
        verbMap = getSignificantVerbs()
        adjMap  = getSignificantAdj()
        cverbMap = getCheapVerbs()

        sentences = getSentences("/home/erdinc/nltk/cs290f_proj/tos_test/")	

	high_sent_count = 0
        for sent in sentences:
                if getSubjectDependencyScore(sent, nounMap, verbMap, adjMap, cverbMap) == 1:
                        high_sent_count += 1

        print "Number of Sentences: %i " % len(sentences)
        print "Qualified Sentences: %i " % high_sent_count


def main():
	#globalSignificantTerms()
	#verbDependency()
	subjectDependency()

main()






'''
        verbList = getVerbList(posTags)
        freqVerb = getMostFreqVerbs(verbList)
        writeFile("Most_Freq_Verbs_50", freqVerb)

        nameList = getNameList(posTags)
        freqName = getMostFreqNames(nameList)
        writeFile("/home/erdinc/nltk/cs290f_proj/stats/Most_Freq_Names_50", freqName)

        sentences = getSentences("/home/erdinc/nltk/cs290f_proj/tos_test/")
        writeFile('google_neg_new', sentences)
'''


