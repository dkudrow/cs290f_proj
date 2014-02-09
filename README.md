# CS290F Project - Daniel Kudrow & Erdinc Korpeoglu

## Applying natural language processing techniques to extract specific
properties from web service privacy policies

### Data
The data lives in the _data/_ directory. The raw text files reside in
_data/texts/_. _fetch.py_ is a python script that retrieves the documents
listed in _url.list_ and sanitizes them. _cats.txt_ contains the categories
for each file. A word 

### Classification
Each classifier determines where a _class label_ can be applied for a given
input. The input is divided into sentences and each sentence can carry a
class label. The class label marks the sentence as relevant to one of the
following questions:

1. What information is collected (what)?
2. How is the information stored/secured (how)?
3. With whom is information shared (who)?
4. Can I delete my information (delete)?

Each sentence is fed to a _feature extractor_ which generates a _feature set_
for it. The classifier can then use the feature set to determine whether
that sentence is relevant. The relevant sentences continue on for semantic
analysis.

## Semantic Analysis
