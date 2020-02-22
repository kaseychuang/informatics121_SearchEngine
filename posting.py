class Posting:
    def __init__(self, docid, freq): # add position and fields later
        self.docid = docid
        self.freq = freq    # change this to tf-idf later
        # self.positions = positions # a list of positions/ints
        # self.fields = fields
        # add a way to keep track if it's a header or bolded?

    def get_docid(self):
        return self.docid

    def get_freq(self):
        return self.freq

    def get_positions(self):
        return self.positions

    def get_fields(self):
        return self.fields