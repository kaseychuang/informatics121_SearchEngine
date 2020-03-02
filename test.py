# test search engine methods

from searchEngine import SearchEngine
se = SearchEngine("index")


print(se.search("cristina lopes", 5))
print(se.search("machine learning", 5))
print(se.search("ACM", 5))
print(se.search("master of software engineering", 5))



# import pickle
#
# file = open("pIndex1.pkl", "rb")
# d = pickle.load(file)
# file.close()
#
# print(len(d))

# for k, v in d.items():
#     #print(k,v)
#     print(k, ": ", v)

# LINKED LIST OR SET UF POSTINGS?
# IF YOU USE A SET, YOU NEED TO IMPLEMENT THE __EQ__ ETC AND HASH

# USE STEMMING TO CUT DOWN ON # OF ENTRIES IN INDICES

# MERGING STRATEGY
# have an index for every letter
# create a partial index
# go through that sorted index and load to memory each letter
# at a time, that way we only have one partial memory and one letter's index open at a time!
# maybe have two partial indices open, one alphabet one
# multiway merging??

# look up the best way to implement a posting?
# will need to add positions later?

# stuck on file 16991??

from collections import OrderedDict
# import json
#
# file_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b",
#                 "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
#                 "o","p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
#
# for name in file_names:
#     file_name = "index/" + name + ".txt"
#     file = open(file_name, 'w')
#     json.dump(dict(), file, indent = 3)
#     file.close()



import indexMerger
import json
from collections import OrderedDict
# import os
#
# #indexMerger.merge_partials("partial_indexes")
# for filename in os.listdir("partial_indexes"):
#     print(filename)


# merged_index = indexMerger.binary_merge("pIndex1.txt", "pIndex2.txt")
#
# with open("merged.txt", "w") as m_index:
#     json.dump(merged_index, m_index, indent = 3)
# m_index.close()

#file = open("index/a.txt", mode = 'r')

#print(file.name)
# index = json.load(file)
# indexMerger.write_pindex_to_disk(index)

#
# l1 = ["hi", "there", "friend"]
# l2 = ["apple", "cherry"]
#
# print(l1 + l2)
# print(l2 + l1)

# file = open("test.txt", 'r')
# p_index = json.load(file)
# indexMerger.write_pindex_to_disk(p_index, "index")

# doesn't get to the last term??

# I'm double writing to the json file?? How do I replace everything?
# do I have to open it as w+

# iterate through each entry
# add it to the appropriate letter index

# book keeping, index the terms and where their position is in the file??
# can keep it in memory, or on disk so you can check it yourself

# can try implementing seek operations with json files
# stick with letter indexes, but can create bookkeeping index
    # make it faster to grab stuff later??

# merge at the end or as we go?

# could open all partial indexes simultaneously and read from each
# DON'T LOAD THEM INTO MEMORY THOUGH!
# by parsing the format of the json, I should be able to grab terms and their postings


