from lxml import etree
from collections import Counter
import os

# Name of the file containing the messages
dir = os.path.dirname(__file__)
fname = os.path.join(dir, os.pardir, "sms.xml")

tree = etree.parse(fname)

# Split the whole document sms content by sms content
sms_bodies = [sms.text for sms in tree.xpath("/corpus/sms/cont")]

# Split the whole document sms content by sms content
sms_sent_to = Counter(sms.text for sms in tree.xpath("/corpus/sms/tel_id"))
