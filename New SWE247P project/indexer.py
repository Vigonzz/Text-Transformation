# Module 3 - Inverted Index

# Citation: AI chat mode was used to assist in structure, understanding, and calculations
# All code was produced by me 

'''
How to run:
1. Activate the venv: source venv/bin/activate
2. cd "New SWE247P project"
3. Empty the inv-index/ folder (removes old shards)
4. python indexer.py

Test mode: set INPUT_DIR to "test-input" at the top of indexer.py
'''

from pathlib import Path

SCRIPT_DIR = (Path(__file__).parent.resolve())

# Join the folders
INPUT_DIR = SCRIPT_DIR / "input-transform"
#Make the output setting
OUTPUT_DIR = SCRIPT_DIR / "inv-index"
# write the doc id SETTING
DOC_IDS_FILE = OUTPUT_DIR / "doc-ids.txt"



# Placeholder functions
def find_documents():
    """ Finds all files in the input folder, sots and assigns the doc ids
     Reads tokens and fills in the input folder, sorting and assigning the doc ID """
    files = []
    # get every path under the input folder
    for path in INPUT_DIR.rglob("*"):
        if path.is_file() and not path.name.startswith("."):
            files.append(path)
    # sort
    files = sorted(files)

    # assign ids:
    docs_ids = {}

    # Get number and paths
    for num, file_path in enumerate(files, start=1):
        real_path = file_path.relative_to(INPUT_DIR)
        docs_ids[num] = real_path
    return docs_ids


def build_index(docs_ids):
    """ Builds the terms to the doc ID and also the position """
    index = {}
    # Loop over the docs
    for doc_id,doc in docs_ids.items():
        full_path = INPUT_DIR / doc
        # Read the file
        content = full_path.read_text(encoding="utf-8")
        tokens = content.split()
        # Loop over the token w/ positions
        for position, term in enumerate(tokens, start=1):
            if term not in index:
                index[term] = {}
            if doc_id not in index[term]:
                index[term][doc_id] = []
            index[term][doc_id].append(position)
    return index

    return index
def write_index(index):
    """ Sort the terms and write the first-letter shards into inv-index file """
    # Sort the terms
    sorted_terms = sorted(index)

    # Group line by shard
    shards = {}
    for term in sorted_terms:
        file_name = shard_name(term)
        if file_name not in shards:
            shards[file_name] = []
        shards[file_name].append(format_line(term, index[term]))
    
    # Writing the shards
    for f_name,list_line in shards.items():
        with open(OUTPUT_DIR / f_name, "w", encoding="utf-8") as f:
            f.write("\n".join(list_line) + "\n")


    # Open the file
    #with open(INDEX_FILE, "w", encoding="utf-8") as write_index:
        #for term in sorted_terms:
        #    term_line = format_line(term, index[term])
        #    write_index.write(f"{term_line}\n")

def write_doc_ids(files):
    """ Write the doc ids """
    with open(DOC_IDS_FILE, "w", encoding="utf-8") as doc_ids:
        for ids, pathing in files.items():
            doc_ids.write(f"{ids}\t{pathing}\n")

def format_line(term, term_info):
    # One piece per doc
    pieces = []
    for doc_id, positions in term_info.items():
        # Get the count
        count = len(positions)
        # Convert to strings
        pos_strings = map(str, positions)
        # Glueing the commas
        pos_text = ",".join(pos_strings)
        # Build the piece
        pieces.append(f"{doc_id}:{count}:{pos_text}")
    # Join the pieces
    postings_text = ";".join(pieces)

    return f"{term} {postings_text}"

def shard_name(term):
    """ Split into first letter shards """
    # A small helper for the shard name
    first_char = term[0]
    if first_char in "a" <= first_char <="z":
        return f"{first_char}.txt"
    
    return f"{first_char}.txt"


# Adding the skeleton
def main():
    print(INPUT_DIR)
    print(OUTPUT_DIR)

    # Create the output folder if it is missing
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    docs_ids = find_documents()
    write_doc_ids(docs_ids)
    index = build_index(docs_ids)
    write_index(index)
    # Test 6
    #print(format_line("market", index["market"]))
    #print(format_line("agricultur", index["agricultur"]))
    # Test 5
    #print(len(index))
    #print(index["market"])
    #print(index["chemic"])



if __name__ == "__main__":
    main()
