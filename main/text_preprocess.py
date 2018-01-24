""" SMS Preprocess  """
import sys
sys.path.append('..')
import time
from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from operator import itemgetter
from polyglot.detect import Detector
from polyglot.text import Text
from textblob import TextBlob
from custom_textblob.textblob_fr import PatternTagger, PatternAnalyzer
import sms_dico.sms
import sms_dico.sms_traduction
import french_dico.french
import antispam

d = antispam.Detector("../french_antispam/antispam_model.dat")
stemmer = FrenchStemmer()
dico_fr = french_dico.french.french.split("\n")
dict_pho_fr = dict()
dico_sms_fr = dict()

for french_sms_word, french_sms_trad in zip(sms_dico.sms.sms_dico.split("\n"), sms_dico.sms_traduction.sms_dico_trad.split("\n")):
    dico_sms_fr.update({ french_sms_word: french_sms_trad })

stop_words = stopwords.words('french')
for x in ['il', 'je', 'tu', 'elle', 'nous', 'vous', 'on']:
    stop_words.remove(x)

def preprocess_sms(list_sms):
    clean_sms = []
    cpt_spam = 0
    start = time.time()
    for id, sms in list_sms:
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
                    word = word.lower()
                    if word in stop_words:
                        continue
                    elif word in dico_fr:
                        sms_res += word + ' '
                    elif word in dico_sms_fr:
                         sms_res += dico_sms_fr[word] + ' '
                    else:
                        sms_res += word + ' '
            except:
                sms_res = ' '

            sms_res = stemmer.stem(sms_res)
            blob = TextBlob(sms_res, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

            clean_sms.append([blob.sentiment[0], blob.sentiment[1], id, sms])

    clean_sms = sorted(clean_sms, key=itemgetter(0, 1))

    print('The preprocess of the sms have been done in ', 
            round(time.time() - start, 2), 'seconds', sep = '')
    print(cpt_spam, 'spam/ad has been deleted')
    return [sms for sms in clean_sms]
