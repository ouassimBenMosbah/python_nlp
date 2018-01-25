import antispam

d = antispam.Detector("antispam_model.dat")

with open('list_spams.txt') as f:
    for spam in f:
        d.train(spam, True)

with open('list_hams.txt') as f:
    for ham in f:
        d.train(ham, False)

d.save()
