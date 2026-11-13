# Module 4: develop a search interface for searching occurrences of words in the corpus
from transform import tokenize, load_stopwords, remove_stopwords, stem_tokens

from nltk import PorterStemmer
from pathlib import Path

# Settings
SCRIPT_DIR = (Path(__file__).parent.resolve())
INDEX_DIR = SCRIPT_DIR / "inv-index"
DOC_IDS_FILE = INDEX_DIR / "doc-ids.txt"
STOPWORDS_FILE = SCRIPT_DIR / "stopwords.txt"

def main():
    # Load the stopwords
    stopwords = load_stopwords(STOPWORDS_FILE)

    # Create cache as an empty dict. 
    stem_cache = {}

    # Create the stemmer (The og alg. give it classic porter results)
    stemmer = PorterStemmer(mode=PorterStemmer.ORIGINAL_ALGORITHM)



    # Test:
    # Testing get_postings
    shard_cache = {}
    print(get_postings("market", shard_cache, INDEX_DIR)[:50])
    print(get_postings("market", shard_cache, INDEX_DIR)[:50])
    print(get_postings("predict", shard_cache, INDEX_DIR)[:50])
    print(get_postings("zzzqqq", shard_cache, INDEX_DIR))
    print(shard_cache.keys())


    # Testing load_shard:
    #shard_test = load_shard(INDEX_DIR / "m.txt")
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

def load_doc_ids(path):
    # Hold the loaded ids
    doc_ids = {}
    # Read the file lines
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            doc_id, doc_path = line.strip().split("\t")
            # Convert the path to display form
            display_path = str(Path(doc_path).parent)
            # Store the ids as an int
            doc_ids[int(doc_id)] = display_path

    return doc_ids

def process_query(query, stopwords, stemmer, stem_cache):
    """ Process the query to match the corpus """
    # Apply the string to tokens
    tokens = tokenize(query)
    # Filter the words
    filtered = remove_stopwords(tokens, stopwords)
    # Stem each token
    stems = stem_tokens(filtered, stemmer, stem_cache)
    return stems

def shard_name(term):
    """ Split into first letter shards """
    # A small helper for the shard name
    first_char = term[0]
    if "a" <= first_char <="z":
        return f"{first_char}.txt"
    
    return "other.txt"

def load_shard(path):
    " Loading a shard into a dict to instantly jump to the key as opposed"
    "to scanning each line "
    # Check for a missing file
    if not path.exists():
        return {}
    shard = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            term, posting = line.strip().split(" ", maxsplit=1)
            # Store shard
            shard[term] = posting
    return shard
    
def get_postings(term, cache_dict, index_dir):
    """ Gets called by the scoring code with a term to handle finding 
     load and remember the shard """
    name = shard_name(term)
    
    if name not in cache_dict:
        # Build the path
        path = index_dir / name 
        # Opens the outer dict and then the inner
        cache_dict[name] = load_shard(path)
    lookup = cache_dict[name].get(term)
    return lookup 


if __name__ == "__main__":
    main()