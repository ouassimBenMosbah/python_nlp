""" Get all the messages from the XML file """
import os
from collections import Counter
from lxml import etree
import re

# Name of the file containing the messages
fname = os.path.join(os.path.dirname(__file__), os.pardir, "sms.xml")

# with open(fname, 'r') as f:
#     corpus = f.read().replace('<3', '(coeur)')
# corpus_modified = re.sub(r"<cont>(?P<a>.*)<(?P<b>.*)</cont>", r"<cont>\g<a> \g<b></cont>", corpus)

# with open(fname, 'w') as f:
#     f.write(corpus_modified)
# tree = etree.parse(fname)

# Split the whole document sms content by sms content
sms_bodies = [sms.text for sms in tree.xpath("/corpus/sms/cont")]

# Split the whole document sms content by sms content
sms_sent_to = Counter(sms.text for sms in tree.xpath("/corpus/sms/tel_id"))

# list of element by either if it is a spam or a ham
sms_spam_ham = [1 if sms.find('spam') is not None else 0 for sms in tree.xpath("/corpus/sms")]