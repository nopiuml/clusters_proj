#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.sparse import *
from scipy import *
import numpy as np
from processing.nltk_scikit import *
import matplotlib.pyplot as plt
from scipy.stats import norm
from operator import itemgetter, attrgetter
from collections import OrderedDict,Counter,defaultdict
import time
from itertools import izip
from sys import getsizeof
import shelve
import threading, Queue
from itertools import *
from sys import argv
import math
import operator
from openpyxl.descriptors.base import Length






class InitialCluster(object):
    def __init__(self, clus_of_toks, docs):
        self.clus_of_toks = clus_of_toks
        self.docs = docs

'''
 This function sorts tf-idf weights of every term of each document. 
 @param csr_mat (tf-idf matrix in csr format)
'''
def sort_tfidfs(csr_mat):
    
  
    all_values_sorted = {}
    
    for i in range(0, csr_mat.shape[0]):
        
        if not (len(csr_mat[i].data)==0): # some terms might be blank 
            
            # i => document
            #print csr_mat[i]
            # col_ind[list] => tokens included in this item
            col_ind = csr_mat[i].indices 
            #print col_ind
            # tf_idf[list] => tf_idf values of each token
            tf_idf = csr_mat[i].data
            
            
            all_values = dict(izip(col_ind,tf_idf))

            # all_values_sorted is a dictionary which has the form of num_of_doc:{token:tfidf, token:tf_idf}
            all_values_sorted[i] = sorted(all_values.items(),key=itemgetter(1),reverse=True)
                       

        
          
    return all_values_sorted


'''
extract significant n-grams from sorted_tf_idf matrix
@param n (n-gram)
@param sorted_tfidfs (dictionary with tf-idf weights of every term)
@param voc (vocabulary)
'''
def sig_words(n,sorted_tfidfs,voc):
    
    clusters = defaultdict(list)
    fo = open("tfidfs.txt", "wb")

    for key,value in sorted_tfidfs.items():
              
            if (len(value)>=n):
                for i in range(0,n):
                    (tokeni,tfidfi) = value[i]
                    clusters[key].append(voc[tokeni])
                    
                    print "%f ===> %s in doc%d \n"% (tfidfi, voc[tokeni],key)
                    fo.write("%f ===> %s in doc%d \n"% (tfidfi, voc[tokeni],key))
                    
                print "=========================== \n" 
                fo.write("===========================\n")    
                
             
    fo.close()
                
    return clusters




"""
Calculate intersection between clusters and documents based on the given overlap
@param cluster
@param doc
@param overlap
"""
def intersect(cluster, doc, overlap):

    intersection_is = list(set(cluster) & set(doc))
    if (len(intersection_is)==overlap):
        return intersection_is
    else:
        return []


"""
Compare two words. If equal, return word. If not ,return false.
@param a 
@param b
"""
def same_word(a,b):
    if(a==b):
        return a
    
    return False


"""
Sequential clustering algorithm.
@param sig_word (significant n-grams)
@param i
@param splitted_dict (splitted data in equal parts)
@param q (queue to save results)
@param n (n-gram)
@param tLock (lock threads)
@param clusters (list with initial vocabulary of clusters)
@param docs (list with initial docs in clusters)
@param sig_words_items (sig_words.items())
@param overlap (given overlap)
"""
          
def clustering(sig_word, splitted_dict, which_thread, q, n, tLock, clusters, docs,sig_words_items, overlap ):
      
   
    common_toks = []
    for key,value in splitted_dict.items():
                                      
                             
        
        # we skip first key,value pair because this pair is the first cluster and we don't need to compare it with itself
        if (not(key==sig_word.keys()[0])):
                                 
                                 

                    print value
                    print clusters
                    print docs
  
                    # lock threads while computing common_tokens             
                    with tLock:
                        
                        # compare clusters with docs and find common tokens       
                        if (n==1):
                                common_toks = [same_word(value,cluster) for cluster in clusters]
                        else:
                            common_toks = [intersect(value,cluster,overlap) for cluster in clusters ] 
                               
                        print common_toks
                           
                    with tLock:
                        # compute indices with non_zero elements of common_toks
                        non_zero = [i for i, e in enumerate(common_toks) if e]
                        non_zero_toks = [common_toks[i] for i in non_zero]
                    
                        # save in a dictionary indices and tokens of common_toks
                        non_zero_dict = dict(zip(non_zero,non_zero_toks))
                        print non_zero_dict

                             
                    if (n==1):
                            with tLock:
                                if(non_zero_toks):
                                        
                                        # choose the longest list
                                        key_is =  max(non_zero_dict.iteritems(), key=operator.itemgetter(1))[0]
                                        value_is = max(non_zero_dict.iteritems(), key=operator.itemgetter(1))[1]
                                        
                                       
                                        docs[key_is].append(key)
                                         
                                        # new cluster is the union of old and new clusters 
                                        clusters[key_is] = list(set(clusters[key_is]) | set(value))
                                   
                                                
                                else:
                                       
                                        clusters.append(value)
                                        docs.append([key])
                    else:
                            with tLock:  
                                    if(non_zero_toks):
                                        
                                        key_is =  max(non_zero_dict.iteritems(), key=operator.itemgetter(1))[0]
                                        value_is = max(non_zero_dict.iteritems(), key=operator.itemgetter(1))[1]
                                        
                                                                       
                                        docs[key_is].append(key)
                                        clusters[key_is] = list(set(clusters[key_is]) | set(value))
                                                
                                    else:
                                       
                                        clusters.append(value)
                                        docs.append([key])
                          
    
    # put results in a queue
    q.put(InitialCluster(clusters,docs)) 
#     return InitialCluster(clusters,docs)
 
    

"""
Split dictionary in equal pieces
@param input_dict 
@param chunks 
"""      
def split_dict_equally(input_dict, chunks):
    
        # Splits dict by keys. Returns a list of dictionaries
        # prep with empty dicts
        return_list = [dict() for idx in xrange(chunks)]
        idx = 0
        for k,v in input_dict.iteritems():
            return_list[idx][k] = v
            if idx < chunks-1:  # indexes start at 0
                idx += 1
            else:
                idx = 0
        return return_list
    
"""
Handling threads
@param sig_word 
@param q 
@param n
@param file1 
@param file2
@param start
@param stop 
@param tLock
@param clusters (list with initial clustes)
@param docs (list with initial docs)
@param sig_words_items
@param overlap
"""    
def handle_threads(sig_word,splitted_dict, q, n, file1, file2, start, stop, tLock, clusters, docs,sig_words_items, overlap):
    
    # overlap between clusters is the half of the significant words
    #overlap = int(n) // 2
    for i in range(start,stop):
  
        ti = threading.Thread(target= clustering, args=(sig_word, splitted_dict[i],"t%d"%i,q,int(n),tLock,clusters, docs, sig_words_items, overlap))
        ti.start()
        result = q.get()
        if (i==stop-1):
            if (n>1):
                for i in result.clus_of_toks:
                    for j in i:
                        file1.write(j+",")
                    file1.write("\n")
                      
                for k in result.docs:
                    for m in k:
                        file2.write(str(m)+",")
                    file2.write("\n")
            if (n==1):
                for i in result.clus_of_toks:
                    file1.write(i+",")
                    file1.write("\n")
                for k in result.docs:
                    file2.write(k+",")
                    file2.write("\n")
          
    file1.close()
    file2.close()
    return result
    
    print "Clusters' number is: %d" % len(result.docs)
    
    

   
        
       
       

  


