from collections import Counter
import unittest
import os
import re
from main import reg_exps as regexs
from main import main as main_prog
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'main'))
import data_getter

class TestRegexs(unittest.TestCase): 
    def setUp(self):
        self.dates = regexs.dates
        self.list_regexs = [
            regexs.regexp_hours,
            regexs.regexp_money,
            regexs.regexp_currency,
            regexs.regexp_email,
            regexs.regexp_tel
        ]

        self.list_sentences_match = [
            'Il faudrait qu\'on se donne rendez-vous demain',
            'Elle est morte mardi?c\'est ca?',
            'resto a 20h!!',
            'ça m\'a couté 19,99e lol',
            'il me doit 100 boules',
            'il va me passé10patates!!'
            'test@yopmail.com',
            'test2@société.io'
            '06.12.34.56.78',
            '0612345678',
            '07 12 34 56 78',
            '06 12 34 5678',
            '+336 12345678'
            'son num é0612345678.'
        ]

        self.list_sentences_no_match = [
            '',
            'Il faudrait qu\'on se voit',
            'il a fait beau',
            'on va manger au resto !',
            'il a 1988 idées',
            'test@com',
            'ce sont ces patates!',
            '06.12.34.56.8',
            '061234567',
            '06 12 34 6 78',
            '0012345678',
            '+216 12 34 56 78'
        ]

    def test_regexs(self):
        for sentence in self.list_sentences_match:
            self.assertTrue(
                any(re.search(regex, sentence) for regex in self.list_regexs) or any(
                    re.search(r'\b' + date + '\\b', sentence) for date in self.dates))
    
    def test_regexs_not_matching(self):
        for sentence in self.list_sentences_no_match:
            self.assertFalse(
                any(re.search(regex, sentence) for regex in self.list_regexs) or any(
                    re.search(r'\b' + date + '\\b', sentence) for date in self.dates))

class TestMethods(unittest.TestCase):
    def setUp(self): 
        self.list_content1 = []
        self.list_content2 = [
            'bonjour',
            'test de contenu',
            'bonsoir',
            '!!!'
        ]
        self.counter_sms_sent1 = Counter()
        self.counter_sms_sent2 = Counter(
            num for num in ['0612345678','0612345678', '0687654321'])


    def test_print_general_stats(self):
        try:
            main_prog.print_general_stats(0, self.list_content1, self.counter_sms_sent1)
            main_prog.print_general_stats(10, self.list_content1, self.counter_sms_sent1)

            main_prog.print_general_stats(10, self.list_content2, self.counter_sms_sent1)
            main_prog.print_general_stats(10, self.list_content2, self.counter_sms_sent2)

            main_prog.print_general_stats(0, self.list_content1, self.counter_sms_sent2)
            
            main_prog.print_general_stats(10, self.list_content1, list(self.counter_sms_sent1))
        except:
            self.fail('print_general_stats raised an exception !')


if __name__ == '__main__':
    unittest.main()
