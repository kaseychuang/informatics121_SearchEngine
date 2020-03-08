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
# doc_dict is <doc, [term postings]>
def get_scores( query_term_list, doc_dict):
    scores = {doc_id:0 for doc_id in doc_dict.keys()}
    #print(doc_dict)

    # tf-idf scoring for now
    for doc_id, postings in doc_dict.items():
        score = 0
        for p in postings:
            score += p["tf-idf"]
        scores[doc_id] += score

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


# gets score based on if it's bolded, linked etc.
def get_doc_analysis_score(doc_id):

    return 0
