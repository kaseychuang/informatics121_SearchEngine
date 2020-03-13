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
        self.soup = ""
        self.text = ""
        self.html_dict = dict()
        self.setup()

    # sets up all the member variables
    def setup(self):
        self.soup = BeautifulSoup(self.markup, "lxml")
        for script in self.soup(["script", "style"]):
            script.decompose()

        self.text = self.soup.get_text()

        # get rid of one letter tokens later??
        self.tokens = tokenizer.get_tokens(self.text)

        self.freq = tokenizer.get_freq_dict(self.tokens)

        self.html_dict = self.get_html_elements()

        # remove duplicate tokens
        self.tokens = set(self.tokens)
        # could potentially run this through a stemmer later!

    def get_tokens(self):
        return self.tokens;

    def get_freq_dict(self):
        return self.freq

    def get_word_freq(self, word):
        return self.freq[word]

    # implement this later
    def calc_authority(self):
        return True

    # parses HTML for certain tags
    # adds all terms that are within those tags and adds them to dictionary
    # key = term
    # value = list of tags ['a', 'b', 'h1' etc]
    def get_html_elements(self):
        # put all terms inside with an empty list
        html_dict = {term:[] for term in self.tokens}

        # use Beautiful soup to get all the tags
        titles = self.soup.find_all("title")
        h1s = self.soup.find_all("h1")
        h2s = self.soup.find_all("h2")
        h3s = self.soup.find_all("h3")
        bolds = self.soup.find_all(["bold", "strong"])

        # get words inside those tags
        for title in titles:
            words = tokenizer.get_tokens(title.findAll(text=True)[0])
            for word in words:
                html_dict[word].append("t")

        for h1 in h1s:
            words = tokenizer.get_tokens(h1.findAll(text=True)[0])
            for word in words:
                html_dict[word].append("h1")

        for h2 in h2s:
            words = tokenizer.get_tokens(h2.findAll(text=True)[0])
            for word in words:
                html_dict[word].append("h2")

        for h3 in h3s:
            words = tokenizer.get_tokens(h3.findAll(text=True)[0])
            for word in words:
                html_dict[word].append("h3")

        for bold in bolds:
            words = tokenizer.get_tokens(bold.findAll(text=True)[0])
            for word in words:
                html_dict[word].append("b")

        return html_dict


    # returns a dictionary that is representative of a posting object
    def get_posting(self, word):
        posting = dict()
        posting["id"] = self.id
        posting["freq"] = self.get_word_freq(word)
        posting["html"] = self.html_dict[word]
        posting["tf-idf"] = 0; # will be calculated later

        return posting


