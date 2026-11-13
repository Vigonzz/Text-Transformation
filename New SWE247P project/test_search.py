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
