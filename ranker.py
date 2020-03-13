# RANKING METHODS!
import math
import json

# returns doc ID list sorted by rank
def rank_docs(query_list, docs_dict):
    # sort the documents based on the scores

    # doc:score pairs
    scores = get_scores(query_list, docs_dict)


    results = [doc_info[0] for doc_info in sorted(scores.items(), key=lambda x: -x[1])]
    #print("results: ", results)

    return results

# RETURN dictionary of docId, score
# doc_dict
# keys = docId
# values = list of (term, posting) tuples
def get_scores(query_term_list, doc_dict):
    print("starting scoring")
    idf_file = open("idfs.txt", "r")
    idf_dict = json.load(idf_file)
    # set up score tracker
    scores = {docId:0 for docId in doc_dict.keys()}

    # tfidf for now
    # for docId, info in doc_dict.items():
    #     scores[docId] += get_doc_tfidf(info, idf_dict)

    # cosine similarity?
    q_vector = get_query_vector(query_term_list, idf_dict)
    print(q_vector)
    for docId, info in doc_dict.items():
        scores[docId] = get_cosine_similarity(q_vector, docId, doc_dict, idf_dict)
        #print(scores[docId])
    # COULD IGNORE LOW TFIDF QUERIES?? DUNNO IF THAT WOULD MAKE IT FASTER
    # MIGHT MAKE IT MORE ACCURATE THOUGH?



    # authority?

    # links/hubs?

    # pagerank?
    # print("scores: ", scores)

    idf_file.close()

    #print(scores)

    return scores


# gets the cosine similarity of a query doc pair
# a single document! Go through all the terms
def get_cosine_similarity(query_vector, doc_id, doc_dict, idf_dict):


    doc_vector = 0
    doc_l2_norm = 0 # for length normalization

    pairs = doc_dict[doc_id]
    for term, posting in pairs:
        # get tf-idf of this term
        tfidf = get_doc_term_tfidf(term, posting, idf_dict)

        doc_vector += tfidf
        #doc_l2_norm += (tfidf ** 2)


  #  l_normalize = math.sqrt(doc_l2_norm) * query_vector
   # print("normalizing factor: ", l_normalize)

   # cosine_sim = query_vector * doc_vector / l_normalize

    # print("normalized: ", cosine_sim)

    return query_vector * doc_vector


def get_query_vector(query_term_list, idf_dict):
    query_vector = 0
    print(query_term_list)
    for term in query_term_list:
        query_vector += get_query_term_tfidf(term, idf_dict)


    return query_vector


# returns the tfidf of that query term
def get_query_term_tfidf(query_term, idf_dict):
    tf = 1 + math.log(1, 10)
    idf = idf_dict[query_term]
    tfidf = tf * idf
    return tfidf


def get_doc_term_tfidf(term, posting, idf_dict):
    tf = posting["freq"]
    tf = 1 + math.log(tf, 10)
    idf = idf_dict[term]

    return tf * idf


# returns the tfidf of that document term
def get_doc_tfidf(term_posting_list, idf_dict):
    # open the idf file
    tfidf = 0
    for term, posting in term_posting_list:
        tf = posting["freq"]
        tf = 1 + math.log(tf, 10)
        idf = idf_dict[term]
        tfidf += tf * idf

    return tfidf


# gets score based on if it's bolded, linked etc.
def get_doc_analysis_score(doc_id):

    return 0
