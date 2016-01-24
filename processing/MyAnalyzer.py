#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nltk.stem.porter import *
from nltk.corpus import stopwords
from twokenize import *
import string
from unidecode import unidecode

"""
Linguistic processing
@param text (raw text to be processed)
"""
def tweetAnalyzer(text):

    # stopword_extraction
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']
    porter = PorterStemmer()
    protected = Protected
    terms_only = []
    # unescape html
    tokenized_unescaped = normalizeTextForTagger(text)


    # tokenize based on the unescaped tokenized_unescaped
    tokens = tokenize(tokenized_unescaped)

    # translate unicode chars to ascii 
    tokens_decode = [unidecode(token) for token in tokens]

    # stopword_removal
    tokens = [token for token in tokens_decode if token not in stop]

    # stemming
    tokens_stem = [porter.stem(token) for token in tokens]

    # return terms_only
    for token in tokens_stem:
        if not (protected.match(token)):
                terms_only.append(token)
    return terms_only
