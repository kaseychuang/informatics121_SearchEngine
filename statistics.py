

class Statistics():
    def __init__(self, filepath):
        self.num_docs = 0
        self.unique_tokens = set()
        self.filepath = filepath

    def add_token(self, word):
        self.unique_tokens.add(word)

    def add_doc(self):
        self.num_docs += 1

    # update file
    def update_stats(self):
        file = open(self.filepath, 'w')

        file.write("Number of Documents: "+ str(self.num_docs))
        file.write("\nNumber of Unique Tokens: " + str(len(self.unique_tokens)))



