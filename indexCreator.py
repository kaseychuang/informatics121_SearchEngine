# create a document parser object?
import zipfile
import json
import documentParser
from statistics import Statistics
import re
from collections import OrderedDict
import indexMerger as im


#SET UP

# create index files
file_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b",
                "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                "o","p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

for name in file_names:
    file_name = "index/" + name + ".txt"
    file = open(file_name, 'w')
    json.dump(dict(), file, indent = 3)
    file.close()

stats = Statistics("stats.txt")

z = zipfile.ZipFile("/Users/kaseychuang/Downloads/developer.zip", mode = 'r')
json_files = z.namelist()

id_urls = dict()
id = 0 # this is the docIDs
file_num = 0 # tracks num of files we've gone through
index_num = 1   # take this out later? (need a diff way to merge?)
partial_index = OrderedDict()

# CREATE PARTIAL INDEXES!

while(file_num < len(json_files)):

    # CREATE A PARTIAL INDEX
    while (file_num < len(json_files)):
        print("file Num: ", file_num)
        # check if json file and not a folder
        if re.match(r".*(\.json)",  json_files[file_num]):
            file = z.open(json_files[file_num], mode='r')
            data = json.load(file)

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

                # append posting to partial index term's postings list
                if token not in partial_index:
                    stats.add_token(token)
                    partial_index[token] = [] # turn this into a linked list later!!


                partial_index[token].append(ds.get_posting(token))

            # close file we just opened
            file.close()

        file_num += 1


        if (len(partial_index) > 200000): # about 25 MB right now
            break


    filename = "partial_indexes/pIndex" + str(index_num) + ".txt"
    with open(filename, "w") as pIndex:
        json.dump(partial_index, pIndex, indent = 4)
    pIndex.close()

    index_num += 1
    partial_index.clear()  # reset partial index
    stats.update_stats()    # update statistics


# close the zip file
z.close()
stats.update_stats()

# WRITE URLS TO DISK (AS A JSON FILE)
with open("urls.txt", "w") as url_file:
    json.dump(id_urls, url_file, indent=4)
url_file.close()

# MERGE PARTIAL INDEXES INTO SINGLE ONE
im.merge_partials("partial_indexes")

# calculate the tf-idf values?

# ADD TF-IDF! (add that into the IndexMerger module later
