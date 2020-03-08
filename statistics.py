

class Statistics():
    def __init__(self, filepath):
        self.num_docs = 0
        self.unique_tokens = set()
        self.filepath = filepath

    def add_token(self, word):
        self.unique_tokens.add(word)

    def add_doc(self):
        self.num_docs += 1

    def get_num_docs(self):
        return self.num_docs

    # update file
    def update_stats(self):
        file = open(self.filepath, 'a')

        file.write("\nNumber of Documents: "+ str(self.num_docs))
        file.write("\nNumber of Unique Tokens: " + str(len(self.unique_tokens)))



