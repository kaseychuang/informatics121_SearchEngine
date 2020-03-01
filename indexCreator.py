# create a document parser object?
import zipfile
import json
import documentParser
from posting import Posting
from statistics import Statistics
import pickle
import re
import sys
from collections import OrderedDict


#SET UP

# create index files
file_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b",
                "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                "o","p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

for name in file_names:
    file_name = "index/" + name + ".txt"
    file = open(file_name, 'w')
    od = OrderedDict()
    json.dump(od, file, indent = 3)

stats = Statistics("stats.txt")

z = zipfile.ZipFile("/Users/kaseychuang/Downloads/developer.zip", mode = 'r')
json_files = z.namelist()

id_urls = dict()
id = 0 # this is the docIDs
#batch = 10000
file_num = 0 # tracks num of files we've gone through
index_num = 1   # take this out later? (need a diff way to merge?)
partial_index = OrderedDict()


while(file_num < len(json_files)):
#while(file_num < 10):

    # CREATE A PARTIAL INDEX
    while (file_num < len(json_files)):
        print("file Num: ", file_num)
        # check if json file and not a folder
        if re.match(r".*(\.json)",  json_files[file_num]):
            file = z.open(json_files[file_num], mode='r')
            #print("FILE: ", file)
            data = json.load(file)
            #print("URL: ", data["url"])

            # keep count of num of docs
            stats.add_doc()
            id = id + 1

            # add to url dictionary
            url = data["url"]
            id_urls[id] = url

            # extract info from markup
            ds = documentParser.DocParser(id, data["content"])

            # creating the posting for each token!
            for token in ds.get_tokens():
                #posting = Posting(id, ds.get_word_freq(token))

                # append posting to partial index term's postings list
                if token not in partial_index:
                    stats.add_token(token)
                    partial_index[token] = [] # turn this into a linked list later!!


                partial_index[token].append(ds.get_posting(token))

            # close file we just opened
            file.close()

        file_num += 1


        # maybe 10 MB at a time instead!!!
        if (len(partial_index) > 200000): # about 25 MB right now
            break

    print("PUTTING PARTIAL INDEX ON DISK!")

    # WRITE TO JSON FILE INSTEAD
    filename = "partial_indexes/pIndex" + str(index_num) + ".txt"
    with open(filename, "w") as pIndex:
        json.dump(partial_index, pIndex, indent = 4)
    pIndex.close()


    # merging methods here???
    # create merge method here
    # takes two file names, which have partial in file?? Or just the first file
    # use pickle

    index_num += 1
    partial_index.clear()  # reset partial index
    #batch = batch + 10000
    stats.update_stats()    # update statistics


# close the zip file
z.close()
stats.update_stats()

# WRITE URLS TO DISK (AS A JSON FILE)
with open("urls.txt", "w") as url_file:
    json.dump(id_urls, url_file, indent=4)
url_file.close()

# merge all the rest of the partial indexes into onedexes
#merges them and writes back to disk into new