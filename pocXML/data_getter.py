""" Get all the messages from the XML file """
import os
from collections import Counter
import lxml

# Name of the file containing the messages
fname = os.path.join(os.path.dirname(__file__), os.pardir, "sms.xml")

tree = lxml.etree.parse(fname)

# Split the whole document sms content by sms content
sms_bodies = [sms.text for sms in tree.xpath("/corpus/sms/cont")]

# Split the whole document sms content by sms content
sms_sent_to = Counter(sms.text for sms in tree.xpath("/corpus/sms/tel_id"))