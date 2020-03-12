# RANKING METHODS!

# returns doc ID list sorted by rank
def rank_docs(query_list, docs_dict):
    # sort the documents based on the scores

    # doc:score pairs
    scores = get_scores(query_list, docs_dict)


    results = [doc_info[0] for doc_info in sorted(scores.items(), key=lambda x: -x[1])]
    print("results: ", results)

    return results

# RETURN dictionary of docId, score
# doc_dict
# keys = docId
# values = list of (term, posting) tuples
def get_scores(query_term_list, doc_dict):
    # set up score tracker
    scores = {docId:0 for docId in doc_dict.keys()}

    # tf-idf scoring for now
    for docId, term_postings in doc_dict.items():
        tfidf_score = 0

        # go through each term_posting
        for tp in term_postings:
            posting = tp[1]
            tfidf_score += posting["tf-idf"]

        scores[docId] += tfidf_score

    # call whatever methods to use elements to calc the scores of a list of docs!

    # how many query terms it contains?

    # cosine similarity?

    # authority?

    # links/hubs?

    # pagerank?
    print("scores: ", scores)


    return scores


# gets the cosine similarity of a query doc pair
def get_cosine_similarity(qi, di):
    # calculate weight of query

    # go through all terms

    return 0

def get_query_tfidf(query_term_list, doc_dict):
    tfidf = 0

    # get term's tf-idf from any of the postings (but how do we know what term is which?)
    #


    return tfidf


# gets score based on if it's bolded, linked etc.
def get_doc_analysis_score(doc_id):

    return 0
