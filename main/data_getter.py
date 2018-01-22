""" Get all the messages from the XML file """
import os
from collections import Counter
from lxml import etree
import re
import time

# Name of the file containing the messages
fname = os.path.join(os.path.dirname(__file__), os.pardir, "sms1.xml")

res = ""
with open(fname, 'r') as f:
    corpus = f.read().split("</sms>")

for sms in corpus:
    sms = sms.replace("\n", "").replace('<3', '(coeur)').replace('&', 'et')
    match = re.search(r"<cont>.*<.*</cont>", sms)
    if match:
        sms = re.sub(r"<cont>(?P<a>.*)</cont>", "<cont>" + match.group()[6:-7].replace('<', ' ') + "</cont>", sms)
    res += sms + "</sms>\n"

with open(fname, 'w') as f:
    f.write(res[:-7])

tree = etree.parse(fname)

# Split the whole document sms content by sms content
sms_bodies = [sms.text for sms in tree.xpath("/corpus/sms/cont")]

# Split the whole document sms content by sms content
sms_sent_to = Counter(sms.text for sms in tree.xpath("/corpus/sms/tel_id"))

# list of element by either if it is a spam or a ham
sms_spam_ham = [1 if sms.find('spam') is not None else 0 for sms in tree.xpath("/corpus/sms")]