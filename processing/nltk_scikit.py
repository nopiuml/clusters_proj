#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import *
import re
import string
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import *
from scipy import *
import numpy as np
from MyAnalyzer import *
from twokenize import *
import matplotlib.pyplot as plt
import time



class ReturnValue(object):
    def __init__(self, tf_idf, voc, number_rw_tweets, raw_tweets):
        self.tf_idf = tf_idf
        self.voc = voc
        self.number_rw_tweets = number_rw_tweets
        self.raw_tweets = raw_tweets


"""
Mathematical processing of raw data - Compute tf-idf weights 
@param n (n-gram)
"""
def extract_sparse(n):

    conn = MongoClient('83.212.109.120')
#     db = conn.twitter_db
    db = conn.london_db

    # fetch field "text" from all documents of collection "t_data"
#     tweet = db.twitter_collection.distinct('text')
    tweet = db.monday_coll.distinct('text')
#     tweet = db.tuesday_coll.distinct('text')
#     tweet = db.wednesday_coll.distinct('text')
#     tweet = db.thursday_coll.distinct('text')
#     tweet = db.friday_coll.distinct('text')
#     tweet = db.saturday_coll.distinct('text')
#     tweet = db.sunday_coll.distinct('text')
#     number_rw_tweets =  len(tweet)
    # turn list to numpy array of tweets
    raw_tweets = np.array(tweet)
    number_rw_tweets =  len(raw_tweets)

    # ngram_range=(1,2),
    tf = TfidfVectorizer(ngram_range=(n,n),analyzer='word',lowercase=False, min_df = 0, tokenizer=tweetAnalyzer)
    tfidf_matrix =  tf.fit_transform(raw_tweets)

    #print tfidf_matrix

    voc = tf.get_feature_names()
    print "Total of documents processed : ",tfidf_matrix.shape[0]
    print "Total of tokens : ",tfidf_matrix.shape[1]


    #print tfidf_matrix.nonzero()[1] # [ 28398  75296 104853 ...,  70300  42268  75122]


    # for i in range(11030,11040):
    #     print "%s <== %i" % (voc[i],i)

    # print tfidf_matrix.shape


#     print "\n"
#     print "===> nltk_scikit.py Done in %fs" % (stop - start)
    return ReturnValue(tfidf_matrix, voc, number_rw_tweets, raw_tweets)

