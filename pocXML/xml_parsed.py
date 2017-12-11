""" Get all the messages from the XML file """
from collections import Counter
import os
from random import randrange
from subprocess import check_output
from nltk.tokenize import word_tokenize
from lxml import etree
import french_dico.french
import french_dico.french_pho
import french_dico.french_stem
import french_dico.french_stem_pho

# Name of the file containing the messages
fname = os.path.join(os.path.dirname(__file__), os.pardir, "sms.xml")

tree = etree.parse(fname)

# Split the whole document sms content by sms content
sms_bodies = [sms.text for sms in tree.xpath("/corpus/sms/cont")]

# Split the whole document sms content by sms content
sms_sent_to = Counter(sms.text for sms in tree.xpath("/corpus/sms/tel_id"))

dict_pho_fr = dict()

for french_pho_word, french_word in zip(french_dico.french_pho.french_pho.split("\n"), french_dico.french.french.split("\n")):
    dict_pho_fr.update({french_pho_word: french_word})


def clean_sms_phonetic(list_sms):
    clean_sms = []
    random_index = randrange(0,len(list_sms))
    for sms in list_sms[random_index:random_index+1]:
        words = word_tokenize(sms, language='french')
        print(words)
        for word in words:
            word_pho = check_output(['espeak', '-v', 'fr', '-x', '-q', word]).decode('utf8').strip()
            if word_pho in dict_pho_fr:
                print(dict_pho_fr[word_pho])
        break
    return list_sms

