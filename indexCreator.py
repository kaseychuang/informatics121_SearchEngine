# create a document parser object?
import zipfile
import json
import documentParser
from statistics import Statistics
import re
from collections import OrderedDict
import indexMerger as im


# -------------------------
# SET UP
# -------------------------

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
id = 0
file_num = 0
index_num = 1   # take this out later? (need a diff way to merge?)
partial_index = OrderedDict()
simhashes = {} # use for detecting duplicate pages

# -------------------------
# CREATE PARTIAL INDEXES!
# -------------------------

while file_num < len(json_files):

    # CREATE A PARTIAL INDEX
    while file_num < len(json_files):
        print("file Num: ", file_num) # FOR DEBUGGING

        # check if json file and not a folder
        if re.match(r".*(\.json)",  json_files[file_num]):
            file = z.open(json_files[file_num], mode='r')
            data = json.load(file)

            # keep count of num of docs, add url to books
            id = id + 1
            url = data["url"]
            id_urls[id] = url

            # extract info from markup
            ds = documentParser.DocParser(id, data["content"])

            # check if don't already have a similar webpage
            if ds.get_simhash() not in simhashes.values():
                # add simhash
                simhashes[id] = ds.get_simhash()
                stats.add_doc() # add doc to statistics

                # add document's terms into index
                for token in ds.get_tokens():
                    if token not in partial_index:
                        stats.add_token(token)
                        partial_index[token] = [] # turn this into a linked list later!!
                    partial_index[token].append(ds.get_posting(token))

            file.close()

        file_num += 1
        if len(partial_index) > 200000: # about 25 MB right now
            break


    filename = "partial_indexes/pIndex" + str(index_num) + ".txt"
    with open(filename, "w") as pIndex:
        json.dump(partial_index, pIndex, indent = 4)
    pIndex.close()

    index_num += 1
    partial_index.clear()  # reset partial index
    stats.update_stats()    # update statistics


z.close()
stats.update_stats()

# WRITE URLS TO DISK (AS A JSON FILE)
with open("urls.txt", "w") as url_file:
    json.dump(id_urls, url_file, indent=4)
url_file.close()


# -------------------------
# CREATE INDEX BY MERGING
# -------------------------

# Create index
im.merge_partials("partial_indexes")
#im.add_tf_idf("index", stats.get_num_docs())

# Create idf dictionary for searching later!
# write that dictionary to a file
im.create_idf_dict("index", stats.get_num_docs())

# add tfidfs
im.add_tf_idf("index", stats.get_num_docs())






# add calc hubs/page rank here?

