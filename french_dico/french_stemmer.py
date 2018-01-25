""" Transform the french dictionary into phonetic stemmed words """
import os
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

os.system('espeak -v fr -f french.txt -x -q > french_pho.txt')

french_stem_pho = []
with open('french_pho.txt', 'r') as f:
    for line in f:
        french_stem_pho += line.split(' ')

french_stem_pho_res = []
for x in french_stem_pho:
    if x.strip('\n '):
        french_stem_pho_res.append(x.strip('\n '))

with open('french_pho.txt', 'w') as f:
    f.write("\n".join(french_stem_pho_res))
