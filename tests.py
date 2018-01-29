import unittest
import os
import re
import main.reg_exps as regexs

class TestMethods(unittest.TestCase): 
    def setUp(self):
        self.dates = regexs.dates
        self.list_regexs = [
            regexs.regexp_hours,
            regexs.regexp_money,
            regexs.regexp_currency,
            regexs.regexp_email,
            regexs.regexp_tel
        ]

    def test_regexs(self):
        list_sentences = [
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

        for sentence in list_sentences:
            self.assertTrue(
                any(re.search(regex, sentence) for regex in self.list_regexs) or any(
                    re.search(r'\b' + date + '\\b', sentence) for date in self.dates))
    
    def test_regexs_not_matching(self):
        list_sentences = [
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

        for sentence in list_sentences:
            self.assertFalse(
                any(re.search(regex, sentence) for regex in self.list_regexs) or any(
                    re.search(r'\b' + date + '\\b', sentence) for date in self.dates))


if __name__ == '__main__':
    unittest.main()
