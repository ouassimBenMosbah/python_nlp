""" SMS Preprocess  """
import time
from nltk.tokenize import word_tokenize
from subprocess import check_output
from random import randrange
import enchant
import sms_dico.sms
import sms_dico.sms_traduction
import french_dico.french
import french_dico.french_pho
import french_dico.french_stem
import french_dico.french_stem_pho

dico_fr = french_dico.french.french.split("\n")
dict_pho_fr = dict()
dico_sms_fr = dict()
d = enchant.Dict('fr_FR')

for french_pho_word, french_word in zip(french_dico.french_pho.french_pho.split("\n"), dico_fr):
    dict_pho_fr.update({ french_pho_word: french_word })

for french_sms_word, french_sms_trad in zip(sms_dico.sms.sms_dico.split("\n"), sms_dico.sms_traduction.sms_dico_trad.split("\n")):
    dico_sms_fr.update({ french_sms_word: french_sms_trad })

def preprocess_sms(list_sms):
    clean_sms = []
    start = time.time()
    for sms in list_sms:
        try:
            sms_res = ''
            words = word_tokenize(sms, language = 'french')
            for word in words:
                if word in dico_sms_fr:
                    sms_res += dico_sms_fr[word] + ' '
                else:
                    sms_res += word + ' '
        except:
            sms_res = ''
        finally:
            clean_sms.append(sms_res)
    print(round(time.time() - start, 2))
    return clean_sms