#!/usr/bin/python

import urllib
import sys
import nltk
import re

textdir = "text/"

urllist = "url.list"
if len(sys.argv) == 2:
    urllist = sys.argv[1]

def clean(html):
    text = nltk.clean_html(html)
    text = re.sub("\\&#58;", ":", text)
    text = re.sub("\\&rsquo;", "'", text)
    text = re.sub("\\&lsquo;", "'", text)
    text = re.sub("\\&rdquo;", "\"", text)
    text = re.sub("\\&ldquo;", "\"", text)
    text = re.sub("\\&\\#039;", "'", text)
    text = re.sub("\\&quot;", "\"", text)
    text = re.sub("\\&amp;", "&", text)
    text = re.sub(" ([\.:,;])", "\g<1>", text)
    return text

urlfile = open(urllist, 'r')

for line in urlfile:
    line = line.split()
    # ignore lines starting with '#'
    if (line[0] == '#'):
        continue
    html = urllib.urlopen(line[1]).read()
    text = clean(html)
    textfile = open(textdir+line[0], 'w')
    textfile.write(text)
    textfile.close
