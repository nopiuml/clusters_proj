from tfidf_clusters import *

def cluster_Details(clusters,tf_voc):
    print "Longer cluster is: "
    print max(clusters.docs,key=len)
    
    max_cl = max(clusters.docs,key=len)
    
    uniq_cl = 0
    
    # clusters longer than 1 
    cl = []
    
    # indices of clusters with len>1
    ind = []
    for clus in clusters.docs:
        if len(clus)==1:
            uniq_cl = uniq_cl + 1
        if len(clus)>1:
            cl.append(clus)
            ind.append((clusters.docs).index(clus))

    print " %d unique clusters" % uniq_cl
    print "clusters with more than 1 doc are the above"
    print cl
    
#     print ind
#     for ind in ind:
#         
#         print clusters.clus_of_toks[ind]
#         print '\n'
        
        
    # get docs of longer cluster after procession
#     for max in max_cl:
#         print max
#         print  sig_word.get(max)
        
        
    # get docs of longer cluster before procession
    raw_tweets = tf_voc.raw_tweets
#     print raw_tweets
#     for max in max_cl:
#         print  raw_tweets.item(max)    
#     list1 =clusters.docs[1]
#      
#     for i in list1:
#              
#         print sig_word.get(i)