""" A POC of a programm that will translate sms words  """

from nltk.tokenize import word_tokenize
from subprocess import check_output
import sms_dico.sms
import sms_dico.sms_traduction
import french_dico.french
import french_dico.french_pho
import french_dico.french_stem
import french_dico.french_stem_pho

    
s = '''Vas y je dois partir ab1to ! Je sais je suis un peu akro mais j'ai HT des pommes à marco, j'ai fais une af'R !
A l1di !
Y'a ok1 mec qui veut acheter des pommes, je vais jamais y ariV put1 ! je veux avanC sur le marché de la pomme.'''
#print(word_tokenize(s))

dict_pho_fr = dict()

for french_pho_word, french_word in zip(french_dico.french_pho.french_pho.split("\n"), french_dico.french.french.split("\n")):
    dict_pho_fr.update({french_pho_word: french_word})


def clean_sms_phonetic(list_sms):
    clean_sms = []
    for sms in list_sms:
        words = word_tokenize(sms, language='french')
        for word in words:
            word_pho = check_output(['espeak', '-v', 'fr', '-x', '-q', word])
            print(word_pho.decode('utf8'))
        break
    return list_sms

dict_sms_fr = dict()

for french_sms_word, french_sms_trad in zip(sms_dico.sms.sms_dico.split("\n"), sms_dico.sms_traduction.sms_dico_trad.split("\n")):
    dict_sms_fr.update({french_sms_word: french_sms_trad})

print(dict_sms_fr['HT'])
with open('sample.txt') as sample:
    for line in sample:
        print(word_tokenize(line))
