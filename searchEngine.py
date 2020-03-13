# pass in the name of the index folder so it can access it
# create a search object so we don't have to pass every time
import json
import re
import ranker
from stemming.porter2 import stem
import time


class SearchEngine:
    def __init__(self, index_folder):
        self.index_folder = index_folder


    # method that gets called to get search results!
    def search(self, query, num_results):
        # create query list, filter out common query words and duplicates
        query_list = query.split()
        query_list = list(set(query_list))

        i = 0
        while i < len(query_list):
            query_list[i] = stem(query_list[i].lower())
            i += 1

        start_time = time.time()
        # returns dictionary of documents and appropriate term postings
        found_docs = self.find_matching_docs(query_list)

        print("Retrival Time: ", (time.time() - start_time))

        # RANK DOCUMENTS
        results = ranker.rank_docs(query_list, found_docs)

        # return urls of results
        urls = self.get_urls(results)
        print(results[:num_results])

        return urls[:num_results]


    # -------------------------
    # RETRIVAL METHODS
    # -------------------------

    # def filter_query(self, query_term_list):
    #     # get rid of duplicates
    #     if len(query_term_list) > 1:
    #         filtered_queries = set()
    #         for term in query_term_list:
    #
    #     else:
    #         return query_term_list



    # gets the appropriate postings for the term
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

    # returns a list of tuples with (docID, [(term, posting)])
    # value is a list of (term, posting) tuples
    def find_matching_docs(self, query_term_list):
        # key = docID, value = list of (term, posting) tuples
        matches = dict()

        # dictionary for term: postings pairs since we are reordering?
        term_postings = dict()
        for term in query_term_list:
            term_postings[term] = self.get_postings(term)

        # sort postings
        terms = [term for term, postings in sorted(term_postings.items(), key = lambda x: len(x[1]))]
        print(terms)

        # add initial postings inside
        first_term = terms[0]
        postings = self.get_postings(first_term)
        for posting in postings:
            pair = (first_term, posting)
            matches[posting["id"]] = [pair]

        # check if only term in the query
        if len(query_term_list) == 1:
            return matches

        # go through list of terms and their postings in terms of the sorted list
        for term in terms[1:]:
            postings = term_postings[term]
            for posting in postings:
                pair = (term, posting)
                if posting["id"] in matches.keys():
                    matches[posting["id"]].append(pair)

    #print("MATCHES: ", matches)

        return matches


    # takes two lists of doc ids and returns a list of all matching docs
    def merge_postings(self, docs1, docs2):
        #print("docs1: ", docs1)
        #print("docs2: ", docs2)
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

    # pass a list of doc IDs
    def get_urls(self, doc_ids):
        file = open("urls.txt", "r")
        url_list = json.load(file)
        urls = []

        for id in doc_ids:
            url = url_list[str(id)]
            urls.append(url)

        return urls

    def get_collection_size(self):
        return self.collecti

        # file = ope`n("urls.txt", "r")
        # urls = []
        # for id in doc_ids:
        #   # print("ID: ", id)
        #     # file.seek(id + 1)
        #     file.seek(100)
        #     line = file.readline()
        #
        #     print(line)
        #
        #     url = line.split()[1][1:-1];
        #    # print(url)
        #     urls.append(url)
        #
        # file.close()
        #
        # return urls


