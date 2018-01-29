""" Get all the messages from the XML file """
import os
from collections import Counter
from lxml import etree
import re
import time

def get_sms(XML_SMS):
    '''
        From an xml fil given in parameter, it returns a tuple containing:
            - a list of sms (a tuple of (id, content))
            - a list of phone number (string)
    '''
    # Name of the file containing the messages
    fname = os.path.join(os.path.dirname(__file__), os.pardir, XML_SMS)

    res = ""
    with open(fname, 'r') as f:
        corpus = f.read().split("</sms>")

    for sms in corpus:
        sms = sms.replace("\n", "").replace('<3', '(coeur)').replace('&', 'et')
        match = re.search(r"<cont>.*<.*</cont>", sms)
        if match:
            sms = re.sub(r"<cont>(?P<a>.*)</cont>", "<cont>" +
                        match.group()[6:-7].replace('<', ' ') + "</cont>", sms)
        res += sms + "</sms>\n"

    with open(fname, 'w') as f:
        f.write(res[:-7])

    tree = etree.parse(fname)

    # Split the whole document sms content by sms content
    sms_bodies = [sms.text for sms in tree.xpath("/corpus/sms/cont")]

    sms_ids = [sms.attrib['id'] for sms in tree.xpath("/corpus/sms")]

    list_sms = list(zip(sms_ids, sms_bodies))

    # Split the whole document sms content by sms content
    sms_sent_to = Counter(sms.text for sms in tree.xpath("/corpus/sms/tel_id"))

    return (list_sms, sms_sent_to)
