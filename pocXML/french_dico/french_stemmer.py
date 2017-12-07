""" Transform the french dictionary into stemmed words """
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("french")

dict_root = set()
# french.txt is the original dictionary
with open('french.txt', 'r') as f:
    for line in f:
        dict_root.add(stemmer.stem(line.strip("\n ")))

# french_stem.txt is the new dictionary
with open('french_stem.txt', 'w') as f:
    f.write("\n".join(sorted(dict_root)))