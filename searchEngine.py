# pass in the name of the index folder so it can access it
# create a search object so we don't have to pass every time
import json
import re
import ranker

class SearchEngine:
    def __init__(self, index_folder):
        self.index_folder = index_folder

    # method that gets called to get search results!
    def search(self, query, num_results):
        # create query list
        query_list = query.split()

        i = 0
        while i < len(query_list):
            query_list[i] = query_list[i].lower()
            i += 1

        # returns dictionary of documents and appropriate term postings
        found_docs = self.find_matching_docs(query_list)

        # RANK DOCUMENTS
        results = ranker.rank_docs(query_list, found_docs)

        # return urls of results
        urls = self.get_urls(results)

        return urls[:num_results]


    # -------------------------
    # RETRIVAL METHODS
    # -------------------------

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

        print("MATCHES: ", matches)

        return matches

    # # returns THE POSTINGS OF all documents that have all the query terms
    # # returns a dictionary <docID, list of postings>
    # # terms not labeled, but doesn't matter (len(postings) = num query terms)
    # def find_matching_docs(self, query_term_list):
    #
    #     # if just one query
    #     if len(query_term_list) == 1:
    #         postings = self.get_postings(query_term_list[0])
    #         return {p["id"]: [p] for p in postings}
    #         #return [p["id"] for p in postings]
    #
    #     # get each postings list of each term
    #     posting_lists = [self.get_postings(t) for t in query_term_list]
    #
    #     # sort the queries by the length of their postings list
    #     posting_lists = sorted(posting_lists, key = lambda x: len(x))
    #
    #     query_num = 1
    #
    #     # grab doc IDs in the first postings list
    #     matching_docs = [p["id"] for p in posting_lists[0]]
    #
    #     while query_num <= len(posting_lists) - 1:
    #         # merge results with next posting
    #         term_docs = [p["id"] for p in posting_lists[query_num]]
    #         matching_docs = self.merge_postings(matching_docs, term_docs)
    #         query_num += 1
    #
    #     # results is the list of doc ids with all queries
    #     # now build the list with docID and the associated postings with it
    #     # MAKE THIS MORE EFFICIENT LATER!
    #     results = dict()
    #     for doc_id in matching_docs:
    #         results[doc_id] = []
    #         for postings in posting_lists:
    #             for p in postings:
    #                 if p["id"] == doc_id:
    #                     results[doc_id].append(p)
    #
    #     return results


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


