# Module 3 - Inverted Index
from pathlib import Path

SCRIPT_DIR = (Path(__file__).parent.resolve())

# Join the folders
INPUT_DIR = SCRIPT_DIR / "input-transform"
#Make the output setting
OUTPUT_DIR = SCRIPT_DIR / "inv-index"

# Placeholder functions
def find_documents():
    """ Finds all files in the input folder, sots and assigns the doc ids """
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
    
    



def build_index():
    """ Reads tokens and fills in the input folder, sorting and assigning the doc ID """
    pass
def write_index():
    """ Sort the terms and write the first-letter shards into inv-index file """
    pass

# Adding the skeleton
def main():
    print(INPUT_DIR)
    print(OUTPUT_DIR)

    # Create the output folder if it is missing
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    docs_id = find_documents()
    print(len(docs_id))



if __name__ == "__main__":
    main()
