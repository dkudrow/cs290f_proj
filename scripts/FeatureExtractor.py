#
# FeatureExtractor.py
#

import os
import random
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag

corpusdir = "../corpus/what_info_we_collect"

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
    nounMap["Data"]     = "N"   
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
    verbMap["use"]      = "V"
    verbMap["share"]    = "V"
    verbMap["collect"]  = "V"
    verbMap["shared"]   = "V"
    verbMap["used"]     = "V"
    verbMap["give"]     = "V"
    verbMap["post"]     = "V"
    verbMap["offer"]    = "V"
    verbMap["disclose"] = "V"
    verbMap["store"]    = "V"
    verbMap["delete"]   = "V"
    verbMap["remove"]   = "V"
    verbMap["uses"]     = "V"

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

def extractNounCount(tagged):
    nounMap = getNounMap()
    conjMap = getConjMap()
    
    nounCount = 0
    recogNoun = False
    inList = False
    for (token, tag) in tagged:
        token = token.lower()
        if tag[:2] == "NN":
            if token in nounMap:
                #print token + ": recognized noun"
                recogNoun = True
                nounCount += 1
            elif inList:
                #print token + ": unrecognized noun in list"
                recogNoun = False
                nounCount += 1
                
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
    return nounCount

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

    features['verbCount'] = extractVerbCount(tagged)
    features['nounCount'] = extractNounCount(tagged)

    return features
  
#def main():
    #fileList = os.listdir(corpusdir)
    #sentences = []
    #doc = fileList[0]
    #for doc in fileList:
        #classif = doc[-3:]
        ##if classif == "pos": continue
        #if classif == "neg": continue
        #f = open(corpusdir + "/" + doc)
        #raw = f.read()
        #sentences = (sent_tokenize(raw))
        #f.close()
        #for sent in sentences:
            #print ""
            #print sent
            #tagged = pos_tag(word_tokenize(sent))
            #print "tag: %s\nverbs: %i\nnouns: %i\n" % (classif, extractVerbCount(tagged, classif), extractNounCount(tagged, classif))
