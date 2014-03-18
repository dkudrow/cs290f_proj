#
# FeatureExtractor.py
#

import os
import random
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.stem.porter import PorterStemmer

corpusdir = "../corpus/what_info_we_collect"
stemmer = PorterStemmer()


def getNounMap():
    nounMap = {}
    nounMap["information"]  = "N"
    nounMap["account"]  = "N"
    nounMap["services"] = "N"
    nounMap["data"]     = "N"
    nounMap["email"]    = "N"
    nounMap["content"]  = "N"
    nounMap["access"]   = "N"
    nounMap["friends"]  = "N"   
    nounMap["device"]   = "N"
    nounMap["cookies"]  = "N"
    nounMap["address"]  = "N"
    nounMap["party"]    = "N"
    nounMap["others"]   = "N"
    nounMap["privacy"]  = "N"
    nounMap["contact"]  = "N"
    nounMap["name"]     = "N"
    nounMap["location"] = "N"
    nounMap["settings"] = "N"
    nounMap["profile"]  = "N"
    nounMap["user"]     = "N"   
    nounMap["location"] = "N"   
    nounMap["username"] = "N"   
                    
    return nounMap

def getConjMap():
    conjMap = {}
    conjMap["and"]      = "J"
    conjMap["or"]       = "J"
    conjMap[","]        = "J"

    return conjMap

def getVerbMap():
    verbMap = {}
    verbMap[stemmer.stem("use")]      = "V"
    verbMap[stemmer.stem("share")]    = "V"
    verbMap[stemmer.stem("collect")]  = "V"
    verbMap[stemmer.stem("shared")]   = "V"
    verbMap[stemmer.stem("give")]     = "V"
    verbMap[stemmer.stem("post")]     = "V"
    verbMap[stemmer.stem("offer")]    = "V"
    verbMap[stemmer.stem("disclose")] = "V"
    verbMap[stemmer.stem("store")]    = "V"
    verbMap[stemmer.stem("delete")]   = "V"
    verbMap[stemmer.stem("remove")]   = "V"

    return verbMap

def extractVerbCount(tagged):
    verbMap = getVerbMap()
    
    verbCount = 0
    curSubj = False
    curPosses = False
    for (token, tag) in tagged:
        token = token.lower()
        # token is a pronoun
        if tag[:3] == "PRP" or tag[:2] == "WP":
            # token is `we'
            if token == "we":
                #print token + ": recognized subject -- pronoun"
                curSubj = True
            # token is a possesive (next noun could be correct subject)
            elif tag[-1] == "$" and token == "our":
                curSubj = False
                curPosses = True
            # token is some other pronoun
            else:
                #print token + ": unrecognized subject -- pronoun"
                curSubj = False
        # token is a noun
        elif tag[:2] == "NN":
            # token is possessed
            if curPosses:
                #print token + ": recognized subject -- possessed noun"
                curSubj = True
            # token is proper noun
        # token is a verb with correct subject
        elif tag[:2] == "VB" and curSubj:
            # token is a recognized verb
            if token in verbMap:
                #print token + ": recognized verb"
                verbCount += 1
            # token is an unrecognized verb
            else:
                #print token + ": unrecognized verb"
                verbCount += 1
                
    #print classif, verbCount
    return verbCount

def extractNounCount(tagged, tagSym):
    nounMap = getNounMap()
    conjMap = getConjMap()
    
    nounCount = 0
    nounList = []
    recogNoun = False
    inList = False
    for (token, tag) in tagged:
        token = token.lower()
        if tag[:2] == "NN":
            if token in nounMap:
                #print token + ": recognized noun"
                recogNoun = True
                nounCount += 1
                nounList.append(token)
            elif inList:
                #print token + ": unrecognized noun in list"
                recogNoun = False
                nounCount += 1
                nounList.append(token)
                
        elif not inList:
            if recogNoun and token in conjMap:
                #print token + ": entering a list"
                recogNoun = False
                inList = True
        else:
            if token in conjMap or tag[:2] == "JJ":
                #print token + ": continuing in list"
                continue
            else:
                #print token + ": leaving list"
                inList = False
                
    #if (nounCount<3 and tagSym=="pos") or (nounCount>=3 and tagSym=="neg"):
        #print tagged
        #print nounList

    return nounCount

def extractNounList(tagged):
    nounMap = getNounMap()
    conjMap = getConjMap()
    
    nounList = []
    recogNoun = False
    inList = False
    for (token, tag) in tagged:
        token = token.lower()
        if tag[:2] == "NN":
            if token in nounMap:
                #print token + ": recognized noun"
                recogNoun = True
                nounList.append(token)
            elif inList:
                #print token + ": unrecognized noun in list"
                #recogNoun = False
                nounList.append(token)
                #nounMap[token] = "N"
                
        elif not inList:
            if recogNoun and token in conjMap:
                #print token + ": entering a list"
                recogNoun = False
                inList = True
        else:
            if token in conjMap or tag[:2] == "JJ":
                #print token + ": continuing in list"
                continue
            else:
                #print token + ": leaving list"
                inList = False
                
    #print classif, nounCount
    return nounList

def extractVerbList(tagged):
    verbMap = getVerbMap()
    
    verbList = []
    curSubj = False
    curPosses = False
    for (token, tag) in tagged:
        token = token.lower()
        # token is a pronoun
        if tag[:3] == "PRP":
            # token is `we'
            if token == "we":
                #print token + ": recognized subject -- pronoun"
                curSubj = True
            # token is a possesive (next noun could be correct subject)
            elif tag[-1] == "$" and token == "our":
                #print token + ": possessive"
                curSubj = False
                curPosses = True
            # token is some other pronoun
            else:
                #print token + ": unrecognized subject -- pronoun"
                curSubj = False
        # token is a noun
        elif tag[:2] == "NN":
            # token is possessed
            if curPosses:
                #print token + ": recognized subject -- possessed noun"
                curSubj = True
            else:
                curSubj = False
        # token is a verb with correct subject
        elif tag[:2] == "VB":
            token = stemmer.stem(token)
            # token is a recognized verb
            if token in verbMap:
                #print token + ": recognized verb"
                verbList.append(token)
            # token is an unrecognized verb
            elif curSubj:
                #print token + ": unrecognized verb"
                verbList.append(token)
                
    #print classif, verbCount
    return verbList

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
    tagged = pos_tag(word_tokenize(sentence))

    for noun in extractNounList(tagged):
        if noun in features:
            features[noun] += 1
        else:
            features[noun] = 1

    for verb in extractVerbList(tagged):
        if verb in features:
            features[verb] += 1
        else:
            features[verb] = 1

    return features
  
def main():
    fileList = os.listdir(corpusdir)
    sentences = []
    visited = []
    for (stem, tag) in [(f[:-4], f[-3:]) for f in fileList]:
        if stem in visited:
            continue
        else:
            visited.append(stem)

        print "Analyzing %s" % stem
        f_pos, f_neg = open(corpusdir + "/" + stem + "_pos"), open(corpusdir + "/" + stem + "_neg")
        f_neg = open(corpusdir + "/" + stem + "_neg")
        raw_pos, raw_neg = f_pos.read(), f_neg.read()
        sent_pos, sent_neg = sent_tokenize(raw_pos), sent_tokenize(raw_neg)
        f_pos.close()
        f_neg.close()

        thresh = 3
        totPos, totNeg = len(sent_pos), len(sent_neg)
        totTag = totPos + totNeg
        truePos = trueNeg = 0
        falsePos = falseNeg = 0

        for sent in sent_pos:
            tagged = pos_tag(word_tokenize(sent))
            verbList = extractVerbList(tagged)
            if len(verbList) >= thresh:
                truePos += 1
            else:
                falseNeg += 1
                print ""
                print sent
                print verbList

        for sent in sent_neg:
            tagged = pos_tag(word_tokenize(sent))
            verbList = extractVerbList(tagged)
            if len(verbList) >= thresh:
                falsePos += 1
                print ""
                print sent
                print verbList
            else:
                trueNeg += 1

        print "Total sentences: %i" % (totTag)
        print "Total negative: %.2f%%" % (float(totNeg) / totTag * 100)
        print "Total positive: %.2f%%" % (float(totPos) / totTag * 100)
        print "True negatives: %.2f%%" % (float(trueNeg) / totNeg * 100)
        print "True positives: %.2f%%" % (float(truePos) / totPos * 100)
        print "False negatives: %.2f%%" % (float(falseNeg) / totPos * 100)
        print "False positives: %.2f%%" % (float(falsePos) / totNeg * 100)
        print ""

