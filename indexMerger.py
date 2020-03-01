import json
from collections import OrderedDict
import os
# module for merging partial indexes in json format

def merge_partials(folder):
    # open the folder, like we did before
    for filename in os.listdir(folder):
        # open the file
        path = folder + "/" + filename
        file = open(path, 'r')
        print(filename)

        p_index = json.load(file)

        write_pindex_to_disk(p_index, "index")

        p_index.clear()

        file.close()


    # while we still have files in the folder

    # open two at a time and merge them
    # write to a disk

    # then if there is only one file left, then just merge that one
    # into the disk

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


        # write to output file??/
        # check if appropriate index letter file open already
        # if not, open it and close the last one?

# assume that the partial index is already open and loaded as a dictionary
def write_pindex_to_disk(pIndex, indexFolderPath):
    # open index folder path file
    pathname = indexFolderPath + "/a.txt"
    f = open(pathname, mode = 'r+')    # not sure if this is read or write

    # variable to hold the current dictionary that is opened
    # (not sure if it's sorted)
    current_index = json.load(f)

    terms = sorted(pIndex.keys())
    for t in terms:
        # check if appropriate letter index open
        first_char = t[0]

        # check if appropriate file is open
        pathname = "index/" + first_char + ".txt"
        if not f.name == pathname:
            # close current index file
            # dump our current dictionary
            write_and_close(f, current_index)

            # open new index file and load index
            f = open(pathname, 'r+')
            current_index = json.load(f)

        # add partial indexes' postings to the index
        # check if t is in the index file already
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


def add_tf_idf(index):
    # go through each letter/number file

    # calculate the tf_idf for each

    # add that to each postings in the postings list

    return True

