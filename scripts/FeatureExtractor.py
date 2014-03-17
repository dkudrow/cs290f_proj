#
# FeatureExtractor.py
#

import os
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag

corpusdir = "../corpus/what_info_we_collect"

def getNounMap():
    nounMap = {}
    nounMap["information"]  = "N"
    nounMap["account"]  = "N"
    nounMap["services"]     = "N"
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

def getSubjMap():
    subjMap = {}
    subjMap["we"]    = "+"
    
    return subjMap

def extractVerbCount(tagged, classif):
    verbMap = getVerbMap()
    subjMap = getSubjMap()
    
    verbCount = 0
    curSubj = False
    for (token, tag) in tagged:
        token = token.lower()
        if tag[:3] == "PRP" or tag[:2] == "WP":
            if token in subjMap:
                print token + ": recognized subject"
                curSubj = True
            else:
                print token + ": unrecognized subject"
                curSubj = False
        elif tag[:2] == "VB":
            if token in verbMap and curSubj:
                print token + ": recognized verb"
                verbCount += 1
                
    #print classif, verbCount
    return verbCount

def extractNounCount(tagged, classif):
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
                
    print classif, nounCount
    return nounCount
   
def main():
    fileList = os.listdir(corpusdir)
    sentences = []
    doc = fileList[0]
    for doc in fileList:
        classif = doc[-3:]
        #if classif == "pos": continue
        f = open(corpusdir + "/" + doc)
        raw = f.read()
        sentences = (sent_tokenize(raw))
        f.close()
        for sent in sentences:
            print ""
            print sent
            tagged = pos_tag(word_tokenize(sent))
            extractVerbCount(tagged, classif)
        
main()