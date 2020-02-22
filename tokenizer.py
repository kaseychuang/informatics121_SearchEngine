# Tokenizer
# use NLTK (tokenizing and stopwords)

# https://www.nltk.org/
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
#from nltk.stem.porter import *
import re

# https://bitbucket.org/mchaput/stemming/src/default/
from stemming.porter2 import stem



#stemmer = PorterStemmer()

# creates tokens and returns list of them
# parameter is the text from the html markup (but how do we take into account the HTML tags?)
def get_tokens(text):
    all_tokens = word_tokenize(text, "english")
    # remove all punctuation and whitespace
    words = []
    for t in all_tokens:
        if not re.match(r"\d|[!\"\#``$%&'©()*”’+,\-./:';<=>?@\[\\\]^_\‘{|}~]", t):
            words.append(t.lower())
    # de capitalize everything

    return words

# stemmer (Porter for now?)
# paramter: a list of words
# kinda jank tbh, maybe just implement this later
def stem_words(words):
    stemmed = []
    for w in words:
        stemmed.append(stem(w))
    return stemmed


# modifies tokens
    # stemming
    # stopwords (USE STOP WORDS IN OUR INDEX)
    # normalization


# creates dictionary with frequencies? for postings?
def get_freq_dict(tokenList):
    if tokenList is not None:
        freq = dict()
        for token in tokenList:
            if token in freq:
                freq[token] += 1
            else:
                freq[token] = 1
        return freq