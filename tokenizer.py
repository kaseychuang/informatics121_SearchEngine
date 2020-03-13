# Tokenizer
# use NLTK (tokenizing and stopwords)
from nltk.corpus import wordnet

# https://www.nltk.org/
from nltk.stem.porter import *

#https://anhaidgroup.github.io/py_stringmatching/v0.3.x/AlphanumericTokenizer.html
from py_stringmatching import AlphanumericTokenizer
# https://bitbucket.org/mchaput/stemming/src/default/
from stemming.porter2 import stem


a_tokenizer = AlphanumericTokenizer()
stemmer = PorterStemmer()

# ALPHANUMERIC
# creates tokens and returns list of them
def get_tokens(text):
    all_tokens = a_tokenizer.tokenize(text)
    # remove all punctuation and whitespace
    words = []
    for t in all_tokens:
        # stem and decapitalize
        # filter out numbers longer than 10
        # filter out non-english words that are longer than 15 characters
        token = stem(t.lower())
        if token.isnumeric() and len(token) < 10:
            words.append(token)
        elif len(token) < 15 or wordnet.synsets(token):
            words.append(token)

    return words


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