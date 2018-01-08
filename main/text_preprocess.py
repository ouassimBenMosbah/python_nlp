""" SMS Preprocess  """
import sys
sys.path.append('..')
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sms_dico.sms
import sms_dico.sms_traduction
import french_dico.french
import antispam
import enchant

d = antispam.Detector("../french_antispam/antispam_model.dat")
dico_fr = french_dico.french.french.split("\n")
dict_pho_fr = dict()
dico_sms_fr = dict()

# for french_pho_word, french_word in zip(french_dico.french_pho.french_pho.split("\n"), dico_fr):
#     dict_pho_fr.update({ french_pho_word: french_word })

for french_sms_word, french_sms_trad in zip(sms_dico.sms.sms_dico.split("\n"), sms_dico.sms_traduction.sms_dico_trad.split("\n")):
    dico_sms_fr.update({ french_sms_word: french_sms_trad })

stop_words = stopwords.words('french')
for x in ['il', 'je', 'tu', 'elle', 'nous', 'vous', 'on']:
    stop_words.remove(x)

def preprocess_sms(list_sms):
    clean_sms = []
    cpt_spam = 0
    start = time.time()
    for sms in list_sms:
        try:
            is_spam = d.score(sms)
        except TypeError:
            is_spam = 0
        if is_spam > 0.99:
            cpt_spam += 1
            continue
        else:
            try:
                sms_res = ''
                words = word_tokenize(sms, language = 'french')
                for word in words:
                    if word in stop_words:
                        continue
                    # elif word in dico_sms_fr:
                    #     sms_res += dico_sms_fr[word] + ' '
                    else:
                        sms_res += word + ' '
            except:
                sms_res = ' '
            finally:
                clean_sms.append(sms_res[:-1])
    print('The preprocess of the sms have been done in ', 
            round(time.time() - start, 2), 'seconds', sep = '')
    print(cpt_spam, 'spam/ad has been deleted')
    return clean_sms