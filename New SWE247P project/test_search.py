 # Testing get_postings
    #print(get_postings("market", shard_cache, INDEX_DIR)[:50])
    #print(get_postings("market", shard_cache, INDEX_DIR)[:50])
    #print(get_postings("predict", shard_cache, INDEX_DIR)[:50])
    #print(get_postings("zzzqqq", shard_cache, INDEX_DIR))
    #print(shard_cache.keys())

    # Testing load_shard:
    #print(len(shard_test))
    #print(shard_test["market"][:100])

    # Testing process_query
    #lower = process_query("market of prediction",stopwords, stemmer, stem_cache)
    #cap = process_query("Market OF Prediction",stopwords, stemmer, stem_cache)
    #will = process_query("The will of the",stopwords, stemmer, stem_cache)
    #bryon = process_query("byron's wife and children",stopwords, stemmer, stem_cache)
    #print(lower)
    #print(cap)
    #print(will)
    #print(bryon)

    #doc_ids = load_doc_ids(DOC_IDS_FILE)
    # Test print for load doc func. 
    #print(len(doc_ids))
    #print(doc_ids[1])

    # Testing parser_postings:
    #market_parsed = parser_postings(get_postings("market", shard_cache, INDEX_DIR))
    #print(len(market_parsed))
    #print(market_parsed[1])
    #print(len(market_parsed[4]))
    #print(parser_postings(None))

    # Score_query
    #print(len(test))
    #print(len(test[0]))
    #print(len(test[1]))

# MORE FOR SCORE_QUERY:
    #terms = process_query("market of prediction", stopwords, stemmer, stem_cache)
   # scores = score_query(terms, shard_cache, INDEX_DIR)
  #  print(len(scores))
 #   print(scores[1])
#    print(score_query([],shard_cache, INDEX_DIR))

    #test=score_query(['market', 'predict'], shard_cache, INDEX_DIR)
    #print(len(test))
    #print(len(test[0]))
    #print(len(test[1]))
# Shortest:
#    t1 = shortest([3,11,15,25],[10,23])
#    t2 = shortest([4],[2])
#    t3 = shortest([1,100],[50])
#    t4 = shortest([5],[5000])
#    print(t1)
#    print(t2)
#    print(t3)
#    print(t4)

#terms = process_query("market of prediction", stopwords, stemmer, stem_cache)
#    scores = score_query(terms, shard_cache, INDEX_DIR)
#    print(len(scores))
#    print(list(scores.items())[:10])
#    print(score_query(['market'], shard_cache, INDEX_DIR)[1])
#    print(score_query(['market', 'market'], shard_cache, INDEX_DIR)[1])