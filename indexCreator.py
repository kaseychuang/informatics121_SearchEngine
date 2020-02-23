# create a document parser object?
import zipfile
import json
import documentParser
from posting import Posting
from statistics import Statistics
import pickle

# Create objects
stats = Statistics("stats.txt")

# test out zip file stuff
z = zipfile.ZipFile("/Users/kaseychuang/Downloads/developer.zip", mode = 'r')
json_files = z.namelist()

id_urls = dict()
id = 0 # this is the docIDs
batch = 10

# go through documents in batches
# for f in json_files:
#     file = z.open(f, mode = 'r') # this is a json file
partial_index = dict()

while (id < batch):
    # TEST WITH ONE FILE FIRST!
    file = z.open(json_files[1], mode = 'r')
    #print("FILE: ", file)
    data = json.load(file)
    #print("URL: ", data["url"])

    # keep count of num of docs
    stats.add_doc()


    # for each document, gives the URL a doc ID and store this where?? (separate file?)
    id = id + 1
    url = data["url"]
    id_urls[id] = url

    # pass the doc to the document parser extract info from markup
    ds = documentParser.DocParser(data["content"])
    print(sorted(ds.get_freq_dict().items()))
    print(len(ds.get_freq_dict().items()))

    # creating the posting for each token!
    for token in ds.get_tokens():
        posting = Posting(id, ds.get_word_freq(token))

        # append posting to partial index term's postings list
        if token not in partial_index:
            stats.add_token(token)
            #partial_index[token] = [] # turn this into a linked list later!!
            partial_index[token] = 0
            # count number of unique tokens here!

        #partial_index[token].append(posting)
        partial_index[token] += 1

    # close file we just opened
    file.close()


# put the posting into the hashtable or disk memory?
# write to disk

file = open("pIndex1.pkl", "wb")
pickle.dump(partial_index, file)
file.close()


# merging methods here???
# create merge method here
# takes two file names, which have partial in file?? Or just the first file
# use pickle


# empty the hashtable before getting next batch
partial_index = dict()
batch = batch + 1000
stats.update_stats()


# close the file
z.close()

# merge all the rest of the partial indexes into onedexes
#merges them and writes back to disk into new