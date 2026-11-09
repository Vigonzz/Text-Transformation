from transform import tokenize, remove_stopwords, stem_tokens, load_stopwords, PorterStemmer

expected = "document describ market strategi carri compani agricultur chemic report predict market share chemic report market statist agrochem pesticid herbicid fungicid insecticid fertil predict sale market share stimul demand price cut volum sale"

# Load the stopwords
stopwords = load_stopwords("stopwords.txt")

# Create the stemmer (The og alg. give it classic porter results)
stemmer = PorterStemmer(mode=PorterStemmer.ORIGINAL_ALGORITHM)

# Create cache as an empty dict. 
stem_cache = {}

sample = "Document will describe marketing strategies carried out by U.S. companies for their agricultural chemicals, report predictions for market share of such chemicals, or report market statistics for agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, stimulate demand, price cut, volume of sales. "

# Apply clean to tokens
tokens = tokenize(sample)
# Filter the words
filtered = remove_stopwords(tokens, stopwords)
# Stem tokens
stems = stem_tokens(filtered, stemmer, stem_cache)
# Turns into space seperated
result = " ".join(stems)

print("Mine: ", result)
print("Expected:", expected)

