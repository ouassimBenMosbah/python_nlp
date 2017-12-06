import re
import regExps
import sys
import time
import xml_parsed

# Decode sms smileys and so on ...
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

if __name__ == '__main__':
    with open('list.txt') as f:
        list_mot_cle = f.read().split("\n")[:-1]

    # Timestamp of the begining of the operations
    start = time.time()

    ##### General stats #####
    x = 3
    print("- Il y a eu", len(xml_parsed.sms_bodies), "messages envoyés.")
    print("#####################################")
    print("Les", x, "numéros les plus appelés sont:")
    for i, (num, number_call) in zip(range(1, x+1), xml_parsed.sms_sent_to.most_common(x)):
        print(i, "- N°:", num, "appelé", number_call, "fois !")
    print("#####################################")

    ##### Filter #####
    '''
    cpt=0
    # We'll check each sms/line
    for body in xml_parsed.sms_bodies:
        if body:
            # If regexp match then print line and go to next sms/line
            if re.search(regExps.regexpMoney, body) or \
                re.search(regExps.regexpHours, body) or \
                re.search(regExps.regexpCurrency, body) or \
                re.search(regExps.regexpEmail, body):
                #print('-', body.translate(non_bmp_map))
                cpt +=1
                continue
            # If any date match then we print the line and go to next sms/line
            for date in regExps.dates:
                regexpDates = r"\b"+date+"\\b"
                if re.search(regexpDates, body):
                    #print('-', body.translate(non_bmp_map))
                    cpt +=1
                    continue
                    break

    print("il y a eu", cpt, "matchs")
    ''' and None

    # We'll check each sms/line
    for body in xml_parsed.sms_bodies:
        if body:
            if any(x in body for x in list_mot_cle):
                print('-', body)
    

    # Timestamp of the end of the operations
    end = time.time()
    print("temps d'execution:", round(end-start, 2), "secondes")
