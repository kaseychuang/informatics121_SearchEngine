# create a document parser object?
import zipfile
import json
import documentParser
from posting import Posting

# test out zip file stuff
z = zipfile.ZipFile("/Users/kaseychuang/Downloads/developer.zip", mode = 'r')
json_files = z.namelist()

id_urls = dict()
id = 0 # this is the docIDs

# go through documents in batches
# for f in json_files:
#     file = z.open(f, mode = 'r') # this is a json file

# designate what a batch is LATER!

# partial dict for now
partial_index = dict()

# TEST WITH ONE FILE FIRST!
file = z.open(json_files[1], mode = 'r')
print("FILE: ", file)
data = json.load(file)
print("URL: ", data["url"])


# for each document, gives the URL a doc ID and store this where?? (separate file?)
id = id + 1
url = data["url"]
id_urls[id] = url

# pass the doc to the document parser extract info from markup
ds = documentParser.DocParser(data["content"])
print(sorted(ds.get_freq_dict().items()))

# creating the posting for each token!
for token in ds.get_tokens():
    posting = Posting(id, ds.get_word_freq(token))

    # append posting to partial index term's postings list
    if token not in partial_index:
        partial_index[token] = [] # turn this into a linked list later!!
    partial_index[token].append(posting)

# close file we just opened
file.close()

print(partial_index)
print(partial_index["town"][0].get_docid())

# put the posting into the hashtable or disk memory?

# merging methods here???
# use pickle




# close the file
z.close()
