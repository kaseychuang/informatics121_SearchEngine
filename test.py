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

# from collections import OrderedDict
# import json
#
# file_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b",
#                 "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
#                 "o","p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
#
# for name in file_names:
#     file_name = "index/" + name + ".txt"
#     file = open(file_name, 'w')
#
# od = OrderedDict()
# od["hi"] = 3
#
# with open("test.txt", "w") as test_file:
#     json.dump(od, test_file)
# test_file.close()

import json

# open a partial index file
partial_index = json.load("pIndex1.txt")


# iterate through each entry
# add it to the appropriate letter index





