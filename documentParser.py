import tokenizer

# CITE THESE???
from bs4 import BeautifulSoup
from lxml import html

# LATER IMPLEMENT STORING HTML TAGS AND WHICH ARE MORE IMPORTANT
# USE TO CALCULATE IMPORTANCE OF EACH WORD
# MAYBE ADD POSITIONING IN HERE LATER??


class DocParser:
    def __init__(self, docid, markup):
        self.markup = markup
        self.tokens = [] # becomes a set later (dunno if this will be an issue)
        self.freq = dict()
        self.id = docid
        self.setup()

    # sets up all the member variables
    def setup(self):
        text = self.get_text(self.markup)

        # get rid of one letter tokens later??
        self.tokens = tokenizer.get_tokens(text)

        self.freq = tokenizer.get_freq_dict(self.tokens)

        # remove duplicate tokens
        self.tokens = set(self.tokens)
        # could potentially run this through a stemmer later!

    def get_text(self, markup):
        soup = BeautifulSoup(markup, 'lxml')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        return text

    def get_tokens(self):
        return self.tokens;

    def get_freq_dict(self):
        return self.freq

    def get_word_freq(self, word):
        return self.freq[word]

    # implement this later
    def calc_authority(self):
        return True

# takes a document
# uses the HTML

# calculate tf-idf thingy
    # keep track of HTML elements such as headers, bold, etc.

    # returns a dictionary that is representative of a posting object
    def get_posting(self, word):
        posting = dict()
        posting["id"] = self.id
        posting["freq"] = self.get_word_freq(word)
       # posting["tf-idf"] = 0; # will be calculated later

        # implement this later
        #posting["positions"] = []
        #posting["fields"] = []

        return posting


