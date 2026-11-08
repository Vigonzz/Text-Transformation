# Violet Gonzalez, November 7, 2026
# Task:
""" 
Develop a program that reads text files and produces other text files with transformed versions of the input text files. 
The transformations should include the following: tokenization, Porter stemming, and word-stopping.
"""

import sys, os, zipfile
# Main function
def main():

    # Find the scripts folders
    script_dir = os.path.dirname(os.path.abspath(__file__))

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
            



if __name__ == "__main__":
    main()