import nltk
import os
from nltk import sent_tokenize

#from WordMatchClassifier import getTagged, getFeatures
#from PositionalClassifier import getTagged, getFeatures
from FeatureExtractor import getTagged, getFeatures

corpusdir = "../corpus/what_info_we_collect"

def main():
    tagged = getTagged(corpusdir)
    featureSet = [(getFeatures(feature), tag) for (feature, tag) in tagged]
    trainSet = featureSet[:]
    testSet = featureSet[:100]
    classifier = nltk.NaiveBayesClassifier.train(trainSet)

    fileList = os.listdir(corpusdir)
    sentences = []
    visited = []
    for (stem, tag) in [(f[:-4], f[-3:]) for f in fileList]:
        if stem in visited:
            continue
        else:
            visited.append(stem)
        print stem

        f_pos, f_neg = open(corpusdir + "/" + stem + "_pos"), open(corpusdir + "/" + stem + "_neg")
        f_neg = open(corpusdir + "/" + stem + "_neg")
        raw_pos, raw_neg = f_pos.read(), f_neg.read()
        sent_pos, sent_neg = sent_tokenize(raw_pos), sent_tokenize(raw_neg)
        f_pos.close()
        f_neg.close()

        falseNeg = falsePos = trueNeg = truePos = 0
        for sent in sent_pos:
            guess = classifier.classify(getFeatures(sent))
            if guess == "POS":
                truePos +=1
            else:
                falseNeg += 1

        for sent in sent_neg:
            guess = classifier.classify(getFeatures(sent))
            if guess == "NEG":
                trueNeg +=1
            else:
                falsePos += 1

        posTags = len(sent_pos)
        negTags = len(sent_neg)
        totTags = posTags + negTags

        #print "Total sentences: %i" % (totTag)
        #print "Total negative: %.2f%%" % (float(negTags) / totTag * Tag100)
        #print "Total positive: %.2f%%" % (float(posTags) / totTag * 100)
        #print "True negatives: %.2f%%" % (float(trueNeg) / negTags * 100)
        #print "True positives: %.2f%%" % (float(truePos) / posTags * 100)
        print "False negatives: %.2f%%" % (float(falseNeg) / posTags * 100)
        print "False positives: %.2f%%" % (float(falsePos) / negTags * 100)
        print ""


    print "Accuracy: %f" % nltk.classify.accuracy(classifier, testSet)
    #classifier.show_most_informative_features(20)

main()
