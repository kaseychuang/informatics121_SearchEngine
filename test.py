import tokenizer


filePath = "file.txt"
file = open(filePath, 'r')

tokens = []
for line in file:
    tokens = tokens + tokenizer.get_tokens(line)

print(tokens)

freqs = tokenizer.get_freq_dict(tokens)
print(freqs)