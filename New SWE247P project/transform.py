# Violet Gonzalez, November 7, 2026
# Task:
""" 
Develop a program that reads text files and produces other text files with transformed versions of the input text files. 
The transformations should include the following: tokenization, Porter stemming, and word-stopping.
"""

import sys, os, zipfile, re
from nltk.stem import PorterStemmer
# Main function
def main():

    # Find the scripts folders
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Building path for stopwords
    stop_path = os.path.join(script_dir, "stopwords.txt")

    # Load the stopwords
    stopwords = load_stopwords(stop_path)

    # Create cache as an empty dict. 
    stem_cache = {}

    # Create the stemmer (The og alg. give it classic porter results)
    stemmer = PorterStemmer(mode=PorterStemmer.ORIGINAL_ALGORITHM)

    # Picking the folder
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.path.join(script_dir, "input-files")

    if not os.path.isdir(root):
        print(f"Folder not found path:{root}")
        sys.exit(1)

    print(f"Processing: {root} ")

    zips = find_zips(root)
    print(f"Found: {len(zips)}")


    test = read_book(zips[0])
    print(len(test))
    print(test[:300])

    clean = strip_gutenberg(test)
    print(len(test))
    print(len(clean))
    print(clean[:300])

    # Testing tokenize / removing stopwords
    tokens = tokenize(clean)
    filtered = remove_stopwords(tokens, stopwords)
    stem = stem_tokens(filtered, stemmer, stem_cache)
    print(len(stem))
    print(stem[:30])




    
def find_zips(root):
    """ Returns a list of the paths of every .zip file """
    paths = []

    # Unpack the three values
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".zip"):
                paths.append(os.path.join(dirpath, name))

    return sorted(paths)

def read_book(zip_path):
    """ Helps bridge between finding the books and transforming them """
    # Open the book
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.endswith(".txt"):
                raw = z.read(name)
                return raw.decode("ascii", errors="ignore")
    return ""
            
def strip_gutenberg(text):
    """ Returns the book without the license header and footer """
    # Find where to book starts and ends
    start = text.find("*** START OF")
    end = text.find("*** END OF")

    # Check
    if start is -1 or end is -1:
        return text
    
    # Find the end of the start line
    line_end = text.find("\n", start)
    return text[line_end + 1: end]

def tokenize(text):
    """ Convert all words to lowercase, identifies what is getting tokenized"""
    l_text = text.lower()
    words = re.findall(r"[a-z]+", l_text)
    # holds words (except for single), our cleaned up list
    tokens = []
    for word in words:
        # Dropping 1 letter tokens
        if len(word) >= 2:
            tokens.append(word)
    return tokens

def load_stopwords(path):
    """ Help load any stopwords, by reading and splitting """
    with open(path) as f:
        content = f.read()
        words = content.split()
        return set(words)
    
def remove_stopwords(tokens, stopwords):
    """ Remove the stop words that have been identified """
    kept = []
    for token in tokens:
        if token not in stopwords:
            kept.append(token)
    return kept

def stem_tokens(tokens, stemmer, cache):
    """ Turn tokens into a stem list and use a dictionary so the the stemmer 
    doesn't have to work our the same word multiple times"""
    stems = []
    for token in tokens:
        if token not in cache:
            cache[token] = stemmer.stem(token)
        stems.append(cache[token])
    return stems 



if __name__ == "__main__":
    main()