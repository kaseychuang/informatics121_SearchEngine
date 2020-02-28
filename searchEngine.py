# pass in the name of the index folder so it can access it
# create a search object so we don't have to pass every time
import json

class SearchEngine:
    def __init__(self, index_folder):
        self.index_folder = index_folder

    def get_postings(self, term):
        postings = []
        # grab first letter/number of the term
        pathname = "index/" + term[0] + ".txt"
        with open(pathname) as letter_index:
            index = json.load(letter_index)
            # search the inverted index and return the postings list (dictionary)
            postings = index[term]
        letter_index.close() # or just keep this open the entire time???
        return postings

    # returns a merged postings list of all the terms in the list
    def merge_postings(self, query_term_list):
        merged_list = []
        # get each postings list of each term
        postings = [self.get_postings(t) for t in query_term_list]

        # sort the queries by the length of their postings list
        postings = sorted(postings, key = lambda x: len(x))


        # start with first two terms and merge, repeat until we get to the end of the list

        # return the merged list
        return merged_list

    # returns postings list, which can be accessed as URLs?
    def search(self, query_list):
        # get merged postings list


        # return the doc ids of the results
        found_docs = [] # list of doc ids
        return found_docs



# MAKE SURE TO PASS QUERY TERMS THROUGH A STEMMER!
