import json
from collections import OrderedDict
import os
import re
import math
# module for merging partial indexes in json format


def merge_partials(folder):
    print("calling")
    # open the folder, like we did before
    for filename in os.listdir(folder):
        # open the file
        if re.match("^.*\.txt$", filename):
            print("FILENAME: ", filename)
            path = folder + "/" + filename
            file = open(path, 'r')
            print(filename)
            p_index = json.load(file)

            print("hi")

            write_pindex_to_disk(p_index, "index")

            p_index.clear()

            file.close()

    print("ending partisl")


# assume that the partial index is already open and loaded as a dictionary
def write_pindex_to_disk(pIndex, indexFolderPath):
    print("calling write to one index")
    # open index folder path file
    pathname = indexFolderPath + "/a.txt"
    f = open(pathname, mode = 'r+')    # not sure if this is read or write
    current_index = json.load(f)

    terms = sorted(pIndex.keys())
    for t in terms:
        # check if appropriate letter index open
        first_char = t[0]

        # check if appropriate file is open
        pathname = "index/" + first_char + ".txt"
        if not f.name == pathname:
            # update and close current index file
            write_and_close(f, current_index)

            # open new index file and load index
            f = open(pathname, 'r+')
            current_index = json.load(f)

        # add partial indexes' postings to the index
        if t in current_index.keys():
            current_index[t] = merge_postings(current_index[t], pIndex[t])
        else:
            current_index[t] = pIndex[t]

    # write last term and close file
    write_and_close(f, current_index)


# clears the file for the updated index
def write_and_close(opened_file, index):
    opened_file.seek(0)
    opened_file.truncate()
    json.dump(index, opened_file, indent=3)
    opened_file.close()


def merge_postings(p1, p2):
    # check which one has lower doc numbers
    docNum1 = p1[0]["id"]
    docNum2 = p2[0]["id"]

    if docNum1 > docNum2: # will never be equal
        return p2 + p1
    else:
        return p1 + p2


def add_tf_idf(index_folder, collection_size):
    # open the folder, like we did before
    for filename in os.listdir(index_folder):
        # check if it's a txt file
        # open the file
        if re.match("^.*\.txt$", filename):
            path = index_folder + "/" + filename

            print(path)
            file = open(path, 'r+')
            print(filename)

            index = json.load(file)

            for term, postings in index.items(): # this gets list of postings
                df = len(index[term]) # might have to change this if we change to a set
                idf = math.log(collection_size / df, 10)
                print("Term: ", term)

                for p in postings:
                    print(p)
                    tf = 1 + math.log(p["freq"], 10)
                    p["tf-idf"] = tf * idf

            write_and_close(file, index)
            index.clear()


# creates file to store idf dictionary
def create_idf_dict(index_folder, collection_size):
    idf_dict = dict()

    for filename in os.listdir(index_folder):

        if re.match("^.*\.txt$", filename):
            path = index_folder + "/" + filename

            print(path)
            file = open(path, 'r+')
            print(filename)

            index = json.load(file)

            for term, postings in index.items():
                df = len(index[term])
                idf = math.log(collection_size / df, 10)
                idf_dict[term] = idf

    with open("idfs.txt", "w") as idf_file:
        json.dump(idf_dict, idf_file, indent=4)
    idf_file.close()


# # returns a dictionary that indexes the index
# # TEST THIS ON A SMALL SAMPLE!
# def create_indexed_index(index_folder):
#     index_dict = dict()
#
#     filename = "indexed_index.txt"
#     file = open(filename, 'w')
#
#     # have to open all the partial indexes one by one
#     # DO THIS AT THE SAME TIME AS WHEN I MAKE THE IDF DICTIONARY!!! TO MAKE MORE EFFICIENT??
#     for filename in os.listdir(index_folder):
#         index_dict[filename] = dict()
#
#         if re.match("^.*\.txt$", filename):
#             path = index_folder + "/" + filename
#             #print(path)
#             file = open(path, 'r+')
#             #print(filename)
#             for term, postings in index.items():
#                 num_lines = 0
#                 (pos, num) += get_term_offset_and_lines(term, postings)
#                 position += pos
#                 num_lines += num
#                 # index it
#                 index_dict[filename][term] = (position, num_lines)
#
#     json.dump(index_dict, file)
#     file.close()
#
# def get_term_offset_and_lines(term, postings):
#     offset = 0
#     num_lines = 0
#     # calc offset for term
#
#     # calc offset for postings
#     for posting in postings:
#         offset, num_lines += get_posting_offset_and_numlines(posting)
#
#     # calc any last offsets
#
#     return (offset, num_lines)
#
#
# # returns offset for this posting
# def get_posting_offset_and_numlines(posting):
#     #CALCULATE NUM LI NES!!!
#     num_lines = 0
#     # start with characters we know will always be there
#     offset = 0
#
#     # id offset
#     offset += 7 # check if this is right
#     id = posting["id"]
#     offset += len(str(id))
#
#     # freq offset
#     offset += 9
#     freq = posting["freq"]
#     offset += len(str(freq))
#
#     # html offset (DOUBLE CHECK THIS)
#     offset += 9
#     html = posting["html"]
#     offset += sum(len(e) for e in html) # element names
#     offset += 2 * len(html) # add "" for each html element
#     if len(html) > 1: # account for commas
#         offset += len(html) - 1
#
#     # tf-idf offset
#     offset += 11
#     tfidf = posting["tf-idf"]
#     offset+= len(str(tfidf))
#
#     # add ending offsets?
#
#     # CALCULATE NUM LINES!!!!
#
#     return (offset, num_lines)
#
#



# NOT USED BUT COULD BE USEFUL IN THE FUTURE

# returns a merged index (from  2 partials) that I can write to disk
def binary_merge(pIndex1, pIndex2):
    # open all partial index files (so we load all their dictionaries)
    file1 = open(pIndex1, mode='r')
    file2 = open(pIndex2, mode='r')

    p_index1 = json.load(file1)
    p_index2 = json.load(file2)

    p1_terms = sorted(list(p_index1.keys()))
    p2_terms = sorted(list(p_index2.keys()))

    # keep pointers to where we are in the partial index
    pointer1 = 0
    pointer2 = 0

    current_index_file = ""

    merged_index = OrderedDict()
    # open this file?

    # Go through all terms in the partial indexes and write to output!
    # will need to alter this if I want to do more than 2 at a time
    while pointer1 < len(p1_terms) or pointer2 < len(p2_terms):
        # get postings list to merge into output
        if pointer1 < len(p1_terms) and pointer2 < len(p2_terms):
            # get lowest termID (lowest alphanumeric starting with a) and process it
            term1 = p1_terms[pointer1]
            term2 = p2_terms[pointer2]

            if term1 < term2:
                merged_index[term1] = p_index1[term1]
                pointer1 += 1
            elif term2 < term1:
                merged_index[term2] = p_index2[term2]
                pointer2 += 1
            # if they both have the same term
            elif term1 == term2:
                # get both postings
                postings1 = p_index1[term1]
                postings2 = p_index2[term2]

                # add merged postings
                merged_index[term1] = merge_postings(postings1, postings2)
                pointer1 += 1
                pointer2 += 1

        #elif pointer1 < 100:
        elif pointer1 < len(p1_terms): # only have terms in
            term = p1_terms[pointer1]
            merged_index[term] = p_index1[term]
            pointer1 += 1
        else: # if we still have terms in partial index 2
            term = p2_terms[pointer2]
            merged_index[term] = p_index2[term]
            pointer2 += 1

    return merged_index

