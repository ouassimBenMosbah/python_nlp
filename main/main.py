''' This program try to detect suspicious messages '''
from __future__ import print_function
from collections import Counter

def main():
    '''
        the main function that will be run by the program
    '''
    ############################################################
    list_sms, sms_sent_to = data_getter.get_sms(XML_SMS)

    print_general_stats(5, list_sms, sms_sent_to)

    list_sms_content = text_preprocess.preprocess_sms(list_sms)
    list_sms_content = [(sms[-2], sms[-1], sms[0]) for sms in list_sms_content]
    ############################################################

    start = start2 = 0

    ############################################################
    os.makedirs(RESULT_DIR)
    output_new_list_sms(list_sms_content, os.path.join(RESULT_DIR, 'new_sms.xml'))
    ############################################################

    ############################################################
    input_list_keywords = input(
        'Would you like to search the keywords from "list.txt" ? (y/N)')
    if input_list_keywords and input_list_keywords.lower() in ['o', 'y']:
        # Timestamp of the begining of the operations
        start = time.time()
        list_keywords = get_list_keywords(list_sms_content, FILE_LIST_KEYWORDS)
        if list_keywords:
            output_new_list_sms(list_keywords, os.path.join(RESULT_DIR, 'keywords.xml'))
        start = time.time() - start
    ############################################################

    ############################################################
    input_regexps = input(
        'Would you like to search for money/dates/time/emails ? (y/N)')
    if input_list_keywords and input_regexps.lower() in ['o', 'y']:
        start2 = time.time()

        list_currency, list_date, list_email, list_tel = get_list_regexp(
            list_sms_content)
        if list_currency:
            output_new_list_sms(list_currency, os.path.join(RESULT_DIR, 'currency.xml'))
        if list_date:
            output_new_list_sms(list_date, os.path.join(RESULT_DIR, 'date.xml'))
        if list_email:
            output_new_list_sms(list_email, os.path.join(RESULT_DIR, 'email.xml'))
        if list_tel:
            output_new_list_sms(list_tel, os.path.join(RESULT_DIR, 'tel.xml'))

        start2 = time.time() - start2
    ############################################################
    # Total execution time for the operations
    print('Search for keywords/moneys/dates/times in',
          round(start + start2, 2), 'seconds')


def print_general_stats(n, list_sms_content, list_sms_numbers):
    '''
        Print general stats.
        By default will display the 3 most called numbers
    '''
    print('-', len(list_sms_content), 'messages has been sent')
    if list_sms_content and list_sms_numbers and isinstance(list_sms_numbers, Counter):
        print('#####################################')
        print('The', n, 'most called numbers are:')
        for i, (num, number_call) in enumerate(list_sms_numbers.most_common(n), 1):
            print(i, '- Num:', num, 'called', number_call, 'times !')
        print('#####################################')


def output_new_list_sms(list_sms_rated, xml_name):
    '''
        Create an xml file from a list of messages.
        Each message should a tuple containing :
        - an id (a unique identifier)
        - a content (string)
        - a score of suspicion (float between -1 and 1)
    '''
    i = 0
    root = Element('corpus')
    root.set('version', '1.0')
    while i < len(list_sms_rated):
        ID, content, score = list_sms_rated[i]
        sms = SubElement(root, 'sms', {'id': str(ID), 'score': str(score)})
        cont = SubElement(sms, 'cont')
        cont.text = content
        i += 1
    ElementTree(root).write(xml_name, method='xml')


def get_list_keywords(list_sms_content, fname):
    '''
        Keep only the messages with one of the word
        of the fname given in parameter.
    '''
    list_keyword = []
    list_res = []

    with open(fname) as f:
        for line in f:
            if line.strip():
                list_keyword.append(line.strip())
    for ID, body, score in list_sms_content:
        if body:
            if any(keyword in body for keyword in list_keyword):
                list_res.append((ID, body, score))
    print('%s keyword found\n' % str(len(list_res)))
    return list_res


def get_list_regexp(list_sms_content):
    ''' Keep only the messages matching with the regexps '''
    list_currency = []
    list_date = []
    list_email = []
    list_tel = []
    for ID, body, score in list_sms_content:
        if body:
            # If regexp match then print line and go to next sms/line
            # Or if any date match then we print the line and go to next
            # sms/line
            if re.search(reg_exps.regexp_money, body) or \
                    re.search(reg_exps.regexp_currency, body):
                list_currency.append((ID, body, score))
            if re.search(
                    reg_exps.regexp_hours,
                    body) or any(
                        re.search(
                            r'\b' + date + '\\b',
                            body) for date in reg_exps.dates):
                list_date.append((ID, body, score))
            if re.search(reg_exps.regexp_email, body):
                list_email.append((ID, body, score))
            if re.search(reg_exps.regexp_tel, body):
                list_tel.append((ID, body, score))
    print('%s regular expressions matched\n' % str(
        len(list_currency) + len(list_date) + len(list_email) + len(list_tel)))
    return (list_currency, list_date, list_email, list_tel)

if __name__ == '__main__':
    import re
    import time
    import os
    import shutil
    import sys
    from xml.etree.ElementTree import Element, SubElement, ElementTree
    import data_getter
    import reg_exps
    import text_preprocess

    # Decode sms smileys and so on ...
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    CURRENT_FILE = os.path.dirname(__file__)
    RESULT_DIR = os.path.join(CURRENT_FILE, 'results')
    FILE_LIST_KEYWORDS = os.path.join(CURRENT_FILE, 'list.txt')
    XML_SMS = 'sms1.xml'
    
    file_missing = False
    if not os.path.exists(FILE_LIST_KEYWORDS):
        print('- The keywords list is missing.')
        file_missing != file_missing
    if not os.path.exists(
        os.path.join(os.path.dirname(__file__), os.pardir, XML_SMS)):
        print('- The XML containing the messages is missing.')
        file_missing != file_missing
    
    if not file_missing:
        if os.path.exists(RESULT_DIR):
            shutil.rmtree(RESULT_DIR, ignore_errors=True)
        main()
