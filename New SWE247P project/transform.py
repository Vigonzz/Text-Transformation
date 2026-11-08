# Violet Gonzalez, November 7, 2026
# Task:
""" 
Develop a program that reads text files and produces other text files with transformed versions of the input text files. 
The transformations should include the following: tokenization, Porter stemming, and word-stopping.
"""

import sys
import os

# Main function
def main():
    # Picking the folder
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "input-files"





if __name__ == "__main__":
    main()