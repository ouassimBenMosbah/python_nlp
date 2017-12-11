""" A POC of a programm that will translate sms words  """

from nltk.tokenize import word_tokenize

if __name__ == '__main__':
    
    s = '''Vas y je dois partir ab1to ! Je sais je suis un peu akro mais j'ai HT des pommes à marco, j'ai fais une af'R !
A l1di !
Y'a ok1 mec qui veut acheter des pommes, je vais jamais y ariV put1 ! je veux avanC sur le marché de la pomme.'''

    with open('sample.txt') as sms:
        for line in sms:
            print(word_tokenize(line))
        #print(word_tokenize(s))


                   
    
       