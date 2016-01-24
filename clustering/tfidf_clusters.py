import numpy as np
import time
import threading
import Queue


from processing.nltk_scikit import *
from thread_cluster import *
from scipy.sparse import *
from scipy import *
import math
from pip._vendor.distlib.compat import raw_input
from cluster_details import *



if __name__ == '__main__':
    
    # for 2 most significant word
    print "Please enter n-gram (1,2,.....n): "
    proc = ">"
    gram = raw_input(proc)
    
    # take n significant from doc based on their tfidf value
    print "Please enter the number of significant words to extract from a document: "  
    proceed = ">"
    n = raw_input(proceed)
    
    
    print "Please enter the overlap between document and clusters: (1,2,3,4...,k words)"
    pr = ">"
    overlap = raw_input(pr)
    
    
    # compute tfidf_matrix for raw_tweets => tf_voc_number_rw_tweets (tf-idf, vocabulary, number of raw tweets)
    tf_voc = extract_sparse(int(gram))
    tfidf_matrix1 = tf_voc.tf_idf
     
    # here is the vocabulary
    voc = tf_voc.voc
    wrd_tw = empty((tfidf_matrix1.shape[0],),dtype=np.float)
    csr_mat = tfidf_matrix1.tocsr()
     
    # sort tokens based on their tfidf_values
    sort_tfidfs = sort_tfidfs(csr_mat)
     
     
    # take n given significant words from docs
    sig_word = sig_words(int(n),sort_tfidfs,voc)
 
 
    # keep track of time to compute clusters
    start = time.time() 
     
    tLock = threading.Lock()
    q = Queue.Queue()   
    
    splitted_dict = split_dict_equally(sig_word, 10)
    file1 = open("cluster_tokens.txt","wb") 
    file2 = open("cluster_docs.txt","wb")
     
     
    clusters = [sig_word.values()[0]]
    docs = [[sig_word.keys()[0]]] 
     
    # 1.threading/clustering 
    clusters = handle_threads(sig_word, splitted_dict, q, n, file1, file2, 0, 10, tLock, clusters, docs, sig_word.items(), int(overlap))
     
    print "number of clusters is: %d"% (len(clusters.docs))
    print clusters.docs
    
    cluster_Details(clusters, tf_voc)
      

    stop = time.time() 
      
    print "number of raw tweets %d " % tf_voc.number_rw_tweets

    print "program terminated in %f" %(stop-start)
    
