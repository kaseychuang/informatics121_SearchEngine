from posting import Posting
import tokenizer
import llist

# CITE THESE???
from bs4 import BeautifulSoup
from lxml import html

# LATER IMPLEMENT STORING HTML TAGS AND WHICH ARE MORE IMPORTANT
# USE TO CALCULATE IMPORTANCE OF EACH WORD
# MAYBE ADD POSITIONING IN HERE LATER??


class DocParser:
    def __init__(self, markup):
        self.markup = markup
        self.tokens = [] # becomes a set later (dunno if this will be an issue)
        self.freq = dict()
        self.setup(self)

    # sets up all the member variables
    def setup(self):
        text = self.get_text(self.markup)
        self.tokens = tokenizer.get_tokens(text)
        self.freq = tokenizer.get_freq_dict(self.tokens)

        # remove duplicate tokens
        self.tokens = set(self.tokens)

    def get_text(self, markup):
        soup = BeautifulSoup(markup, 'lxml')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        return text

    def get_word_freq(self, word):
        return self.freq[word]

# takes a document
# uses the HTML

# calculate tf-idf thingy
    # keep track of HTML elements such as headers, bold, etc.

