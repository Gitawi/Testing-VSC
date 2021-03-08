#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""

Created on Mon Dec 30 09:43:23 2013

@author: JanB
"""
import hashlib
import sqlite3
import os
import csv
import time
#from time import sleep
#cProfile.run('FileListing.FileListing()')
import logging


""" Hur att skriva ut ett dictionary som en textfil och sedan läsa tillbaka den 
Två olika metoder, en som skriver direkt och en som delar upp dictionariet på läsbara rader
Den med läsbara rader får jobba lite mer med att få rätt variabeltyper = alltid str vid skrivning"""





def PutDictPerLine(dicten,txtfile):
        with open(txtfile,'w') as file:
            file.write("dicten = { \n")
            for k in dicten.keys():
                file.write("'%s':'%s', \n" % (k, dicten[k]))
                file.write("\n")
            file.write("}")

def PullDictPerLine(dictfile):
    with open('slask\\file1.py','r') as file:
        fcontent= file.read()
    filestr = fcontent.replace("\n","")
    liststr = filestr.split(" = ",2)   # Splittrar strängen i dictnamn resp dictsträngen själv
    dictname = liststr[0]
    dictstr = liststr[1] 
    dict = eval(dictstr)
    for k in dict.keys():
        try:
            bb = dict[k] = int(dict[k])
        except ValueError:
            try:
                aa = dict[k] = float(dict[k])
            except ValueError:
                continue
    return dict


def PutDictDirekt(dicten):
    with open('slask\\file2.py', 'w') as f:
        print(dicten, file=f)
    return

def PullDictDirekt():
    with open('slask\\file2.py', 'r') as f:
        content = f.read(); dic = eval(content);
    return dic



    
if __name__ == '__main__':
    logging.basicConfig(level=0)
    dictin = {'Heading':'För Maskinläsning', 'Avser:': 'Rådmansö', 'Kostnad:': 123.50, 'Periodfrån:': 191101}
    txtfile = 'slask\\file1.py'
    print("dictin", dictin)
    PutDictPerLine(dictin,txtfile)
    #logging.info("Klart m PutDict")    
    dictout = PullDictPerLine(txtfile)
    print("dictout", dictout)
    logging.info("klart m PullDict")

    logging.shutdown()    

    