""" A POC of a programm that will extract some suspicious messages """
import re
import time
import sys
import reg_exps
import data_getter
import text_preprocess 
import treetaggerwrapper
import pprint

def print_general_stats(n = 3, list_sms_content = data_getter.sms_bodies, 
                        list_sms_numbers = data_getter.sms_sent_to):
    ''' 
        Print general stats. 
        By default will display the 3 most called numbers 
    '''
    print("-", len(list_sms_content), "messages has been sent")
    print("#####################################")
    print("The", n, "most called numbers are:")
    for i, (num, number_call) in zip(range(1, n+1), list_sms_numbers.most_common(n)):
        print(i, "- Num:", num, "called", number_call, "times !")
    print("#####################################")

def words_tagging(list_sms_content):
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR='../treetagger')
    tags = tagger.tag_text(list_sms_content)
    tags2 = treetaggerwrapper.make_tags(tags)
    pprint.pprint(tags2)

def remove_spams(list_sms_content):
    ''' Return the list of sms after removing the spams '''
    return list_sms_content

def get_list_keywords(list_sms_content, fname = 'list.txt'):
    ''' Keep only the messages with one of the word of the fname given in parameter. '''

    list_keyword = []
    list_index = []
    index = 0
    cpt_keyword = 0

    with open(fname) as f:
        for line in f:
            if line.strip():
                list_keyword.append(line.strip())
    for body in list_sms_content:
        if body:
            if any(x in body for x in list_keyword):
                #print('-', body)
                cpt_keyword += 1
                list_index.append(index)
        index += 1
    return (list_index, cpt_keyword)

def get_list_regexp(list_sms_content):
    ''' Keep only the messages matching with the regexps '''
    cpt_regexp = 0
    list_index = []
    index = -1
    for body in list_sms_content:
        index += 1
        if body:
            # If regexp match then print line and go to next sms/line
            if re.search(reg_exps.regexp_money, body) or \
                re.search(reg_exps.regexp_hours, body) or \
                re.search(reg_exps.regexp_currency, body) or \
                re.search(reg_exps.regexp_email, body):
                #print('-', body.translate(non_bmp_map))
                cpt_regexp += 1
                list_index.append(index)
                continue
            # If any date match then we print the line and go to next sms/line
            for date in reg_exps.dates:
                regexp_dates = r"\b"+date+"\\b"
                if re.search(regexp_dates, body):
                    #print('-', body.translate(non_bmp_map))
                    cpt_regexp += 1
                    list_index.append(index)
                    break
    return (list_index, cpt_regexp)

def main():
    # Decode sms smileys and so on ...
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    print_general_stats()

    list_sms_content = text_preprocess.preprocess_sms(data_getter.sms_bodies)

    list_sms_content = remove_spams(list_sms_content)

    start = start2 = 0

    ############################################################

    # Tagging words

    # words_tagging(list_sms_content)

    ############################################################

    ############################################################
    input_list_keywords = input('Would you like to search the keywords from "list.txt" ? (Y/N)')
    if input_list_keywords and input_list_keywords.lower() in ['o', 'y']:
        # Timestamp of the begining of the operations
        start = time.time()
        list_index_keywords, cpt_keyword = get_list_keywords(list_sms_content)
        start = time.time() - start
    ############################################################

    ############################################################
    input_regexps = input('Would you like to search for money/dates/time/emails ? (Y/N)')
    if input_list_keywords and input_regexps.lower() in ['o', 'y']:
        start2 = time.time()
        list_index, cpt_regexp = get_list_regexp(list_sms_content)
        start2 = time.time() - start2
    ############################################################

    # Total execution time for the operations
    print("Execution time :", round(start + start2, 2), "seconds")

    try:
        print(cpt_keyword, "Keywords found")
    except NameError as e:
        print("0 Keyword found")

    try:
        print(cpt_regexp, "Regular expressions matched")
    except NameError as e:
        print("0 Regular expression found")


if __name__ == '__main__':
    main()