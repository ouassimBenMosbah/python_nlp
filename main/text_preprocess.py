''' SMS Preprocess  '''
from __future__ import print_function
from operator import itemgetter
import os
import sys
import time
import antispam
from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from custom_textblob.textblob_fr import PatternTagger, PatternAnalyzer
import french_dico.french
import sms_dico.sms
import sms_dico.sms_traduction

CURRENT_FILE = os.path.dirname(__file__)
d = antispam.Detector(os.path.join(CURRENT_FILE, os.pardir, 'french_antispam', 'antispam_model.dat'))
stemmer = FrenchStemmer()
dico_fr = french_dico.french.french.split('\n')
dict_pho_fr = dict()
dico_sms_fr = dict()

for french_sms_word, french_sms_trad in zip(sms_dico.sms.sms_dico.split(
        '\n'), sms_dico.sms_traduction.sms_dico_trad.split('\n')):
    dico_sms_fr.update({french_sms_word: french_sms_trad})

stop_words = stopwords.words('french')

def preprocess_sms(list_sms):
    '''
        Take into parameter a lits of messages.
        Return the same list of messages with
        a new suspicion rate and an objectivity rate
    '''
    clean_sms = []
    cpt_spam = 0
    start = time.time()
    for ID, sms in list_sms:
        try:
            is_spam = d.score(sms)
        except TypeError:
            is_spam = 0

        if is_spam > 0.99:
            cpt_spam += 1
            clean_sms.append([1.0, 0, ID, sms])
        else:
            try:
                sms_res = ''
                words = word_tokenize(sms, language='french')
                for word in words:
                    word = word.lower()
                    if word in stop_words:
                        continue
                    elif word in dico_fr:
                        sms_res += stemmer.stem(word) + ' '
                    elif word in dico_sms_fr:
                        sms_res += stemmer.stem(dico_sms_fr[word]) + ' '
                    else:
                        sms_res += stemmer.stem(word) + ' '
            except BaseException:
                sms_res = ' '

            blob = TextBlob(sms_res, pos_tagger=PatternTagger(),
                            analyzer=PatternAnalyzer())

            clean_sms.append([blob.sentiment[0], blob.sentiment[1], ID, sms])

    clean_sms = sorted(clean_sms, key=itemgetter(0, 1))

    print('The preprocess of the sms have been done in ',
          round(time.time() - start, 2), 'seconds', sep='')
    print(cpt_spam, 'spam/ad has been detected\n')
    return clean_sms
