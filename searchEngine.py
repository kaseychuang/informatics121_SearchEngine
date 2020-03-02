# pass in the name of the index folder so it can access it
# create a search object so we don't have to pass every time
import json
import re

class SearchEngine:
    def __init__(self, index_folder):
        self.index_folder = index_folder

    def get_postings(self, term):
        postings = []   # will need to change this if we change the postings list type
        pathname = "index/" + term[0] + ".txt"

        with open(pathname) as letter_index:
            index = json.load(letter_index)

            # search the inverted index and return the postings list (dictionary)
            postings = index[term]
        letter_index.close()
        index.clear()
        return postings

    # returns a all documents that have all the query terms
    def find_matching_docs(self, query_term_list):

        # if just one query
        if len(query_term_list) == 1:
            postings = self.get_postings(query_term_list[0])
            return [p["id"] for p in postings]

        # get each postings list of each term
        posting_lists = [self.get_postings(t) for t in query_term_list]

        # sort the queries by the length of their postings list
        posting_lists = sorted(posting_lists, key = lambda x: len(x))
        #print("sorted: ", postings)

        # if just one query

        # start with first two terms and merge, repeat until we get to the end of the list
        query_num = 1
        #results = postings[0]
        # grab first postings lists by id
        results = [p["id"] for p in posting_lists[0]]

        #print("results: ", results)
        while query_num <= len(posting_lists) - 1:
            # merge results with next posting
            query_docs = [p["id"] for p in posting_lists[query_num]]
            results = self.merge_postings(results, query_docs)
            query_num += 1

        return results

    # takes two lists of doc ids and returns a list of all matching docs
    def merge_postings(self, docs1, docs2):
        # set up pointers
        p1 = 0
        p2 = 0

        merged = []

        while p1 < len(docs1) and p2 < len(docs2):

            if docs1[p1] == docs2[p2]:
                merged.append(docs1[p1])
                p1 += 1
                p2 += 1
            elif docs1[p1] > docs2[p2]:
                p2 += 1
            else:
                p1 += 1

        return merged

    # returns postings list, which can be accessed as URLs?
    def search(self, query, num_results):
        # create query list
        query_list = query.split()
        # make them lowercase
        i = 0
        while i < len(query_list):
            query_list[i] = query_list[i].lower()
            i += 1

        #print("query list: ", query_list)

        # return the doc ids of the results
        found_docs = self.find_matching_docs(query_list) # list of postings
        #print("found docs: ", found_docs)

        file = open("urls.txt", "r")
        url_list = json.load(file)
        #print(type(url_list))

        # grab urls using the doc ids
        # USE SEEK METHOD TO MAKE IT FASTER?? BECAUSE WE KNOW THE FORMAT

        # LATER SORT THE LIST BY COSINE SIMULARITY!!!
        # ADD OTHER SEARCH REFINEMENT METHODS!

        urls = []

        #print(found_docs)

        i = 0
        while i < num_results:
            id = str(found_docs[i])
            #print(id)
            url = url_list[id]
            urls.append(url)
            i += 1

        return urls



# MAKE SURE TO PASS QUERY TERMS THROUGH A STEMMER!
