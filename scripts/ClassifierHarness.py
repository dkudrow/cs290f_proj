import nltk

#from WordMatchClassifier import getTagged, getFeatures
#from PositionalClassifier import getTagged, getFeatures
from FeatureExtractor import getTagged, getFeatures

CORPDIR = "../corpus/"
SUBDIR = "how_we_use_info/"

def main():
    tagged = getTagged(CORPDIR + SUBDIR)
    featureSet = [(getFeatures(feature), tag) for (feature, tag) in tagged]
    trainSet = featureSet[:]
    testSet = featureSet[:100]
    classifier = nltk.NaiveBayesClassifier.train(trainSet)
    #print nltk.classify.accuracy(classifier, testSet)
    falseNeg = 0
    falsePos = 0
    trueNeg = 0
    truePos = 0
    for (sent, tag) in tagged:
        guess = classifier.classify(getFeatures(sent))
        if tag == guess:
            if tag == "POS":
                truePos += 1
            else:
                trueNeg += 1
        else:
            if tag == "POS":
                falsePos += 1
            else:
                falseNeg += 1

    totTags = len(tagged)
    posTags = 0
    for (sent, tag)  in tagged:
        if tag == "POS":
            posTags += 1

    print "Total tags: %i" % totTags
    print "Positive tags: %i" % posTags
    print "Negative tags: %i" % (totTags - posTags)
    print "False Negatives: %i " % falseNeg
    print "False Positives: %i " % falsePos
    print "True Negatives: %i " % trueNeg
    print "True Positivies: %i " % truePos
    print nltk.classify.accuracy(classifier, testSet)
    classifier.show_most_informative_features(20)

main()
