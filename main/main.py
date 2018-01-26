""" A POC of a programm that will extract some suspicious messages """
import re
import time
import sys
import reg_exps
import data_getter
import text_preprocess
from pprint import pprint
from xml.etree.ElementTree import Element, SubElement, ElementTree
import nltk
from nltk.tokenize import word_tokenize


def print_general_stats(n, list_sms_content, list_sms_numbers):
    '''
        Print general stats.
        By default will display the 3 most called numbers
    '''
    print("-", len(list_sms_content), "messages has been sent")
    print("#####################################")
    print("The", n, "most called numbers are:")
    for i, (num, number_call) in enumerate(list_sms_numbers.most_common(n), 1):
        print(i, "- Num:", num, "called", number_call, "times !")
    print("#####################################")


def output_new_list_sms(list_sms_rated, xml_name):
    i = 0
    root = Element('corpus')
    root.set('version', '1.0')
    while i < len(list_sms_rated):
        id, content, score = list_sms_rated[i]
        sms = SubElement(root, 'sms', {'id': str(id), 'score': str(score)})
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
    for id, body, score in list_sms_content:
        if body:
            if any(keyword in body for keyword in list_keyword):
                list_res.append((id, body, score))
    print('%s keyword found\n' % str(len(list_res)))
    return list_res


def get_list_regexp(list_sms_content):
    ''' Keep only the messages matching with the regexps '''
    list_currency = []
    list_date = []
    list_email = []
    list_tel = []
    for id, body, score in list_sms_content:
        if body:
            # If regexp match then print line and go to next sms/line
            # Or if any date match then we print the line and go to next
            # sms/line
            if re.search(reg_exps.regexp_money, body) or \
                    re.search(reg_exps.regexp_currency, body):
                list_currency.append((id, body, score))
            if re.search(
                reg_exps.regexp_hours,
                body) or any(
                re.search(
                    r"\b" + date + "\\b",
                    body) for date in reg_exps.dates):
                list_date.append((id, body, score))
            if re.search(reg_exps.regexp_email, body):
                list_email.append((id, body, score))
            if re.search(reg_exps.regexp_tel, body):
                list_tel.append((id, body, score))
    print('%s regular expressions matched\n' % str(
        len(list_currency) + len(list_date) + len(list_email) + len(list_tel)))
    return (list_currency, list_date, list_email, list_tel)


def main():
    ############################################################
    list_sms, sms_sent_to = data_getter.get_sms(XML_SMS)

    print_general_stats(5, list_sms, sms_sent_to)

    list_sms_content = text_preprocess.preprocess_sms(list_sms[:1000])
    list_sms_content = [(sms[-2], sms[-1], sms[0]) for sms in list_sms_content]
    ############################################################

    start = start2 = 0

    ############################################################
    output_new_list_sms(list_sms_content, 'results/new_sms.xml')
    ############################################################

    ############################################################
    input_list_keywords = input(
        'Would you like to search the keywords from "list.txt" ? (y/N)')
    if input_list_keywords and input_list_keywords.lower() in ['o', 'y']:
        # Timestamp of the begining of the operations
        start = time.time()
        list_keywords = get_list_keywords(list_sms_content, FILE_LIST_KEYWORDS)
        if list_keywords:
            output_new_list_sms(list_keywords, 'results/keywords.xml')
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
            output_new_list_sms(list_currency, 'results/currency.xml')
        if list_date:
            output_new_list_sms(list_date, 'results/date.xml')
        if list_email:
            output_new_list_sms(list_email, 'results/email.xml')
        if list_tel:
            output_new_list_sms(list_tel, 'results/tel.xml')

        start2 = time.time() - start2
    ############################################################

    # Total execution time for the operations
    print("Search for keywords/moneys/dates/times in",
          round(start + start2, 2), "seconds")


if __name__ == '__main__':
    # Decode sms smileys and so on ...
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    FILE_LIST_KEYWORDS = 'list.txt'
    XML_SMS = "sms1.xml"
    main()
