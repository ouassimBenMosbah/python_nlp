""" A POC of a programm that will extract some suspicious messages """
import re
import time
import sys
import reg_exps
import data_getter
import text_preprocess 
import treetaggerwrapper
from pprint import pprint
import nltk
from nltk.tokenize import word_tokenize
from nltk.chunk.regexp import ChunkRuleWithContext, ChunkString

def print_general_stats(n = 3, list_sms_content = data_getter.sms_bodies, 
                        list_sms_numbers = data_getter.sms_sent_to):
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

# def words_tagging(list_sms_tokenized):
#     tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR='../treetagger')
#     list_sms_tagged = []
#     for sms in list_sms_tokenized:
#         tags = tagger.tag_text(sms)
#         list_sms_tagged.append(treetaggerwrapper.make_tags(tags))
#     return list_sms_tagged

# def chunk(list_sms_tagged):
#     new_list_tagged = []
#     for sms_tagged in list_sms_tagged:
#         new_sms_tagged = []
#         for _, pos, lemma in sms_tagged:
#                 new_sms_tagged.append((lemma, pos))
# #####################################
#         new_list_tagged.append(new_sms_tagged)
#     chunkGram = "Tag: {<PRO:PER|NOM>+<VER.*><NOM>}"""
#     chunkParser = nltk.RegexpParser(chunkGram, loop=2)
#     for sms_tagged in new_list_tagged:
#         chunked = chunkParser.parse(sms_tagged)
#         chunked.draw()

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
            # Or if any date match then we print the line and go to next sms/line
            if re.search(reg_exps.regexp_money, body) or \
                re.search(reg_exps.regexp_hours, body) or \
                re.search(reg_exps.regexp_currency, body) or \
                re.search(reg_exps.regexp_email, body) or \
                any(re.search(r"\b"+date+"\\b", body) for date in reg_exps.dates):
                cpt_regexp += 1
                list_index.append(index)
                continue
    return (list_index, cpt_regexp)

def main():
    # Decode sms smileys and so on ...
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    ############################################################
    print_general_stats()

    list_sms_content = text_preprocess.preprocess_sms(data_getter.sms_bodies)
    ############################################################
    
    start = start2 = 0

    ############################################################
    list_sms_tokenized = [word_tokenize(sms, language ='french') for sms in list_sms_content]
    # Tagging words
    # list_sms_tagged = words_tagging(list_sms_tokenized)
    #chunk(list_sms_tagged)

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
    print("Search for keywords/moneys/dates/times in", round(start + start2, 2), "seconds")

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