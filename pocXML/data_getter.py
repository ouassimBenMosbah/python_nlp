""" Get all the messages from the XML file """
import os
from collections import Counter
from lxml import etree

# Name of the file containing the messages
fname = os.path.join(os.path.dirname(__file__), os.pardir, "sms.xml")

tree = etree.parse(fname)

# Split the whole document sms content by sms content
sms_bodies = [sms.text for sms in tree.xpath("/corpus/sms/cont")]

# Split the whole document sms content by sms content
sms_sent_to = Counter(sms.text for sms in tree.xpath("/corpus/sms/tel_id"))

# list of element by either if it is a spam or a ham
sms_spam_ham = [sms.text for sms in tree.xpath("/corpus/sms/spam")]
