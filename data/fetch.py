#!/usr/bin/python

import nltk
import os.path
import re
import sys
import urllib
import unidecode

rawdir = "raw/"
labdir = "labels/"

# fetch all of the documents in a file of the form
#    <name_of_document> <url_of_document>
def getFromList(urllist):
    urlfile = open(urllist, 'r')
    for line in urlfile:
        line = line.split()
        if (line[0] == '#'):
            continue
        get(line[0], line[1])

# retrieve a document from the url and add it to the corpus
def get(tag, url):
    print "\nFetching `%s'..." % (url)
    html = urllib.urlopen(url).read()
    text = html2ascii(html)
    print "    > saving raw file in %s%s" % (rawdir, tag)
    rawfile = open(rawdir+tag, 'w')
    rawfile.write(text)
    rawfile.close
    if os.path.isfile(labdir+tag):
        response = raw_input("    > labeled file already exists, overwrite? [y/n] ")
        if (not response) or (response[0] != "y"):
            return
    print "    > saving labeled file in %s%s" % (labdir, tag)
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(text)
    labfile = open(labdir+tag, 'w')
    for sent in sents:
        if sent != "\n":
            labfile.write("label_none " + re.sub("\n", "", sent) + "\n\n")
    labfile.close

# clean the html and character encoding from a web document
def html2ascii(html):
    encoding = "utf-8"
    print "    > decoding: `%s'" % (encoding)
    getEncoding = re.search("charset=[\"']?([^ >\"']*)", html)
    if getEncoding:
        encoding = getEncoding.group(1).lower()
    print "    > cleaning html"
    text = nltk.clean_html(html)
    text = unidecode.unidecode(text.decode(encoding))
    text = re.sub("\\&#58;", ":", text)
    text = re.sub("\\&rsquo;", "'", text)
    text = re.sub("\\&lsquo;", "'", text)
    text = re.sub("\\&rdquo;", "\"", text)
    text = re.sub("\\&ldquo;", "\"", text)
    text = re.sub("\\&\\#x27;", "'", text)
    text = re.sub("\\&\\#039;", "'", text)
    text = re.sub("\\&\\#064;", "@", text)
    text = re.sub("\\&quot;", "\"", text)
    text = re.sub("\\&copy;", "(c)", text)
    text = re.sub("\\&gt;", ">", text)
    text = re.sub("\\&amp;", "&", text)
    text = re.sub("\\&ndash;", "-", text)
    text = re.sub("\\&mdash;", "-", text)
    text = re.sub("\\&OElig;", "OE", text)
    text = re.sub("\\&bull;", "", text)
    text = re.sub(" ([\.:,;])", "\g<1>", text)
    return text

getFromList("url.list")
