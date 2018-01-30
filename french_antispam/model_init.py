import antispam
import os

CURRENT_FILE = os.path.dirname(__file__)
d = antispam.Detector(os.path.join(CURRENT_FILE, 'antispam_model.dat'))

with open(os.path.join(CURRENT_FILE, 'list_spams.txt')) as f:
    for spam in f:
        d.train(spam, True)

with open(os.path.join(CURRENT_FILE, 'list_hams.txt')) as f:
    for ham in f:
        d.train(ham, False)

d.save()
