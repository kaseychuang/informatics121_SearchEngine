import pickle

file = open("pIndex2.pkl", "rb")
d = pickle.load(file)
file.close()

for k, v in d.items():
    #print(k,v)
    print(k, ": ", v)

# 55482