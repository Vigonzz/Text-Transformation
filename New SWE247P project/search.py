# Module 4: develop a search interface for searching occurrences of words in the corpus
from transform import tokenize, load_stopwords, remove_stopwords, stem_tokens

from nltk import PorterStemmer
from pathlib import Path

import time

# Settings
SCRIPT_DIR = (Path(__file__).parent.resolve())
INDEX_DIR = SCRIPT_DIR / "inv-index"
DOC_IDS_FILE = INDEX_DIR / "doc-ids.txt"
STOPWORDS_FILE = SCRIPT_DIR / "stopwords.txt"

def main():
    # Load the stopwords
    stopwords = load_stopwords(STOPWORDS_FILE)

    # Create the stemmer (The og alg. give it classic porter results)
    stemmer = PorterStemmer(mode=PorterStemmer.ORIGINAL_ALGORITHM)

    # Create cache as an empty dict. 
    stem_cache = {}
    shard_cache = {}
    doc_ids = load_doc_ids(DOC_IDS_FILE)

    # Startup Message:
    print(f"Welcome...{len(doc_ids)} were loaded. To exit the program type 'exit'")

    while True:
        try:
           user = input("Q> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("Closing program...Goodbye")
            break

        # Account for user exiting out of program 
        if user in ["quit", "exit"]:
            print("Closing program...Goodbye")
            break

        # Blank line argument
        if not user:
            continue

        # Process the query
        # Setting the timer
        start = time.perf_counter()
        terms = process_query(user, stopwords, stemmer, stem_cache)
        if not terms:
            print("Not a searchable term! ^_^ Try another word?")
            continue

        scores = score_query(terms, shard_cache, INDEX_DIR)
        print_top10(scores, doc_ids)
        # Calc current time
        print(f"Search your term took: {time.perf_counter() - start:.3f}s")
        print()
    
 
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

def parser_postings(posting):
    """ Translate the index text format into a dict so python can compute. Re
     turns an empty dict for missing terms """
    # Handle for a missing term
    if posting is None:
        return {}
    # Gets filled with one doc per loop and chop the 
    # string into a chunk
    postings = {}
    pieces = posting.split(";")

    # Take the doc chunks
    for entry in pieces:
       doc_id, _ , positions_str = entry.split(":")
       pos_strings = positions_str.split(",")
       # Convert to an int
       positions = []
       # Take one position string at a time
       for p in pos_strings:
           # convert to a num and add to the list
           positions.append(int(p))
           postings[int(doc_id)] = positions
    return postings

def score_query(terms, shard_cache, index_dir):
    """ Takes the processed query terms from Score_counts and Score_positions
    and return the docs relevancy in the form of a dict of doc and score """
    term_postings = []
    for term in terms:
        term_postings.append(parser_postings(get_postings(term, shard_cache, index_dir)))
    
    # Create the accumulator 
    scores = {}
    for t in term_postings:
        for doc, positions in t.items():
            scores[doc] = scores.get(doc, 0) + len(positions)
    
    # Loop over pair numbers
    for k in range(len(terms) - 1):
        if terms[k] == terms[k + 1]:
            continue

        # Parsed dicts:
        a = term_postings[k]
        b = term_postings[k + 1]
        for doc in a:
            if doc not in b:
                continue
            # Add the position score
            dist = shortest(a[doc], b[doc])
            scores[doc] += 1 / dist
    return scores

def shortest(pos_a, pos_b):
    """ A two pointer walk over the two sorted position lists.
     Return the smallest gap between the two """
    
    i = 0
    j = 0
    best = float("inf")

    while i < len(pos_a) and j < len(pos_b):
        # Get the gap distance 
        gap = abs(pos_a[i] - pos_b[j])
        # Measure the gap 
        if gap < best:
            best = gap
        # Steer the pointer for the comparison
        if pos_a[i] < pos_b[j]:
            i += 1
        else:
            j += 1
    return best

def print_top10(scores, doc_ids):
    """ Ranked path (top ten) get printed for having the highest score
    the ties fo into the lower doc id """
    # Sort 
    sorted_id = sorted(scores.items(), key=lambda x: -x[1])

    # Take the top 10
    top10 = sorted_id[:10]
    if not scores:
        print("No results")
        return top10
    # Header for results
    print("Top 10 results:")

    for i, (doc, score) in enumerate(top10, start=1):
        path = doc_ids[doc]
        # Alignment
        print(f"{i:2}. {path}  ")



if __name__ == "__main__":
    main()