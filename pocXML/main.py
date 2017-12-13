""" A POC of a programm that will extract some suspicious messages """
import re
import time
import sys
import reg_exps
import data_getter
import text_preprocess

# Decode sms smileys and so on ...
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

if __name__ == '__main__':
    ##### General stats #####
    x = 3
    print("-", len(data_getter.sms_bodies), "messages has been sent")
    print("#####################################")
    print("The", x, "most called numbers are:")
    for i, (num, number_call) in zip(range(1, x+1), data_getter.sms_sent_to.most_common(x)):
        print(i, "- Num:", num, "called", number_call, "times !")
    print("#####################################")

    ##### Clean data #####
    data_getter.sms_bodies = text_preprocess.preprocess_sms(data_getter.sms_bodies)
    print(data_getter.sms_bodies[:10])

    
    ##### Filter #####
    start = start2 = 0
    ############################################################
    # Keep only the messages with one of the word of the list.txt
    input_list_keywords = input('Would you like to search the keywords from "list.txt" ? (Y/N)')
    if input_list_keywords[0].lower() in ['o', 'y']:
        list_keyword = []
        cpt_keyword = 0

        # Timestamp of the begining of the operations
        start = time.time()

        with open('list.txt') as f:
            for line in f:
                if line.strip():
                    list_keyword.append(line.strip())
        for body in data_getter.sms_bodies:
            if body:
                if any(x in body for x in list_keyword):
                    #print('-', body)
                    cpt_keyword += 1
        start = time.time() - start
    ############################################################

    ############################################################
    # Keep only the messages matching with the regexps
    # We'll check each sms
    input_regexps = input('Would you like to search for money/dates/time/emails ? (Y/N)')
    if input_regexps[0].lower() in ['o', 'y']:
        cpt_regexp = 0
        start2 = time.time()
        for body in data_getter.sms_bodies:
            if body:
                # If regexp match then print line and go to next sms/line
                if re.search(reg_exps.regexp_money, body) or \
                    re.search(reg_exps.regexp_hours, body) or \
                    re.search(reg_exps.regexp_currency, body) or \
                    re.search(reg_exps.regexp_email, body):
                    #print('-', body.translate(non_bmp_map))
                    cpt_regexp += 1
                    continue
                # If any date match then we print the line and go to next sms/line
                for date in reg_exps.dates:
                    regexp_dates = r"\b"+date+"\\b"
                    if re.search(regexp_dates, body):
                        #print('-', body.translate(non_bmp_map))
                        cpt_regexp += 1
                        break
        start2 = time.time() - start2
    ############################################################

    # Timestamp of the end of the operations
    end = time.time()
    print("Execution time :", round(start + start2, 2), "seconds")

    try:
        print(cpt_keyword, "Keywords found")
    except NameError as e:
        print("0 Keyword found")

    try:
        print(cpt_regexp, "Regular expressions matched")
    except NameError as e:
        print("0 Regular expression found")
