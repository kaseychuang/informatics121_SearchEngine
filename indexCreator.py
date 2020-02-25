# create a document parser object?
import zipfile
import json
import documentParser
from posting import Posting
from statistics import Statistics
import pickle
import re

# Create objects
stats = Statistics("stats.txt")

# test out zip file stuff
z = zipfile.ZipFile("/Users/kaseychuang/Downloads/developer.zip", mode = 'r')
json_files = z.namelist()
print(len(json_files))


id_urls = dict()
id = 0 # this is the docIDs
batch = 10000
file_num = 0
index_num = 1

# go through documents in batches
# for f in json_files:
#     file = z.open(f, mode = 'r') # this is a json file
partial_index = dict()

while(file_num < len(json_files)):
#while(file_num < 10):

    # index this batch of files
    while (file_num < batch and file_num < len(json_files)):
        print("file Num: ", file_num)
        # check if json file and not a folder
        if re.match(r".*(\.json)",  json_files[file_num]):
            file = z.open(json_files[file_num], mode = 'r')
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
            ds = documentParser.DocParser(data["content"])

            # creating the posting for each token!
            for token in ds.get_tokens():
                posting = Posting(id, ds.get_word_freq(token))

                # append posting to partial index term's postings list
                if token not in partial_index:
                    stats.add_token(token)
                    partial_index[token] = [] # turn this into a linked list later!!
                   # partial_index[token] = 0
                    # count number of unique tokens here!

                partial_index[token].append(posting)
                #partial_index[token] += 1

            # close file we just opened
            file.close()

        file_num += 1


    # WRITE PARTIAL INDEX TO DISK
    filename = "pIndex" + str(index_num) + ".pkl"
    file = open(filename, "wb")
    pickle.dump(partial_index, file)
    file.close()


    # merging methods here???
    # create merge method here
    # takes two file names, which have partial in file?? Or just the first file
    # use pickle


    # empty the hashtable before getting next batch
    index_num += 1
    partial_index = dict()  # reset partial index
    batch = batch + 10000
    stats.update_stats()    # update statistics


# close the zip file
z.close()

# WRITE URLS TO DISK (AS A JSON FILE)
with open("urls.txt", "w") as url_file:
    json.dump(id_urls, url_file, indent=4)
url_file.close()

# merge all the rest of the partial indexes into onedexes
#merges them and writes back to disk into new