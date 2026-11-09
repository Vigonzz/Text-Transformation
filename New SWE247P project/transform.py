# Violet Gonzalez, November 7, 2026
# Task:
""" 
Develop a program that reads text files and produces other text files with transformed versions of the input text files. 
The transformations should include the following: tokenization, Porter stemming, and word-stopping.
"""

# This program uses the assistance of AI for step breakdown, debugging, and Demo presentation prep. 
# https://claude.ai/share/44be8aaf-7b5a-4fcc-bc1c-8cb0bf7da496
# ALL CODE WAS CREATED BY ME

import sys, os, zipfile, re
from nltk.stem import PorterStemmer
# Main function
def main():

    # Find the scripts folders
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Sets the top-level output folder input_transform
    out_root = os.path.join(script_dir, "input-transform")


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

    for zip_path in zips:
        # Read the book
        text = read_book(zip_path)
        # Clean the words
        clean = strip_gutenberg(text)
        # Error handling
        if clean == text:
            print("No Markers" + os.path.basename(zip_path))
        # Apply clean to tokens
        tokens = tokenize(clean)
        # Filter the words
        filtered = remove_stopwords(tokens, stopwords)
        # Stem tokens
        stems = stem_tokens(filtered, stemmer, stem_cache)
        # Write the output
        write_output(zip_path, root, out_root, stems)
        # Progress print
        print(os.path.basename(zip_path))

    #clean = strip_gutenberg(test)
    #print(len(test))
    #print(len(clean))
    #print(clean[:300])

    # Testing tokenize / removing stopwords
    #tokens = tokenize(clean)
    #filtered = remove_stopwords(tokens, stopwords)
    #stem = stem_tokens(filtered, stemmer, stem_cache)
    #print(len(stem))
    #print(stem[:30])

    
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
    # Find where to book starts
    start = text.find("START OF THE PROJECT GUTENBERG")
    # Check for wording diff
    if start == -1:
        start = text.find("START OF THIS PROJECT GUTENBERG")
    
    # Find where the book ends
    end = text.find("END OF THE PROJECT GUTENBERG")
    # Check for ending word difference
    if end == -1:
        end = text.find("END OF THIS PROJECT GUTENBERG")

    # Fallback if neither versions exist 
    if start == -1 or end == -1:
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
    # Extra stop words to add on
    extra = {"will"}
    with open(path) as f:
        content = f.read()
        words = content.split()
        return set(words) | extra
    
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

def write_output(zip_path, root, out_root, stems):
    # Get te path and swap zip for txt
    rel_path = os.path.relpath(zip_path, root)
    rel_txt = os.path.splitext(rel_path)[0] + ".txt"

    # Builds path of output file by putting the mirrored path inside input-transform
    out_path = os.path.join(out_root, rel_txt)
    # Strips the filename off, leaves the folder that file lives in
    out_dir = os.path.dirname(out_path)

    # Creates a folder chain if its missing
    os.makedirs(out_dir, exist_ok=True)

    # Create a new file
    with open(out_path, "w") as f:
        f.write(" ".join(stems))


if __name__ == "__main__":
    main()