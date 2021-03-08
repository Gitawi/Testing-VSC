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
import PyPDF2
from PyPDF2 import PdfFileReader
#import pdftotext


"""
 sys.setdefaultencoding('utf-8') Farlig function nu deletad tydligen

print ("   ".format(text.encode("utf-8")))   funkar med win-cmd chcp 852, 437 men med unicodehex (CP65001 i cmd window ger "unknown codepage" och hängning from Python)
Att "tvinga fram encoding till "utf-8" även av Unicode-strängar verkar få Python att släppa igenom print till consolen (cmd).
Om man redirectar till en Out.txt så blir det sen rätt om man öppnar i Notepad.exe
"""
slask = "slask\\"
dbfile = slask+"fillista.db"
csvOutput = slask+"csvOutput.csv"

def PyPDF2datafind(path):
    """"
    Hämtar text ur PDFer men är inte helt konsistent. Ibland måste pdferna "saniteras" och OCRas igen för att kunna läsas och ändå 
    kommer alla sidor inte alltid med. Dessutom är PDFerna sådana att texten kommer inte ut logiskt utan lite blandat så att man
    kan inte säkert söka på något ledord eller mening och sen hoppas på att nästa del i texten t.ex. är en faktura summa
    """

    dot = path.rfind(".")
    ext = path[dot:]
    txt = ""
    NP = -1

    if ext.upper() == ".PDF" : 
      
        # Creating a pdf file object.
        pdf = open(path, "rb")
 
        # Creating pdf reader object.
        pdf_reader = PyPDF2.PdfFileReader(pdf)
 
        # Checking total number of pages in a pdf file.
        NP = pdf_reader.numPages
        for i in range(0,NP-1):
            page = pdf_reader.getPage(i)
            xx = page.extractText()
            txt = txt + page.extractText()
        pdf.close()
    else:
        txt = ext + " not pdf"


    return [NP , txt]
 
  

    
  

def md5_of_file(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
       for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()
        
def sqlte2csv(cursor):
    with open(csvOutput, 'wb') as f:
        writer = csv.writer(f)
        #writer.writerow([i[0] for i in cursor.description])
        writer.writerows(cursor)

def FileListing():
    """
    200111 - Fillistningen och placeringen av data i SQLite fungerar bra både med bara filerna ur ett directory med listOfFiles = [f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir, f))]
    eller med att gå igenom hela trädet med os.path.walk()
    """

    # Initiera databas
    db = sqlite3.connect(dbfile)
    #db = sqlite3.connect(':memory:')
    cur = db.cursor()
    
    cur.execute('''DROP TABLE IF EXISTS main.fileTable''')
    cur.execute('''CREATE TABLE main.fileTable(stamp TEXT, NoPages INTEGER, Content TEXT,  fN TEXT, fS INTEGER, fAT TEXT, fMT INTEGER, fCT TEXT, fSize INTEGER, dN TEXT, fDTime TEXT, fMD5 TEXT)''')
    db.commit()
    logging.info('DB skapad och klart')
    
    
    
    # Set the directory to fetch fillist from

    rootDir = 'PDFer f test'
    #rootDir = 'D:\Dropbox\___Ark\_Kvitton'
    logging.info("rootdir: " + rootDir)
    
    
    xx=0

    listOfFiles = [f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir, f))]

    
    for fname in listOfFiles:
        xx = xx+1

          
        path = os.path.join(rootDir, fname)
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
        fatime = time.strftime('%Y%m%d %H:%M:%S',time.gmtime(atime))
        fmtime = time.strftime('%Y%m%d %H:%M:%S',time.gmtime(mtime))
        fctime = time.strftime('%Y%m%d %H:%M:%S',time.gmtime(ctime))
        fmd5 = md5_of_file(path)
        PyPDF2data = PyPDF2datafind(path)
        NP = PyPDF2data[0]
        Cont = PyPDF2data[1]
        logging.debug(' {0:5}  {1:25}  {2:35} - {3:20}'.format( xx, fname, atime, fatime, fmd5))
        cur.execute('''INSERT INTO main.fileTable ( stamp, NoPages, Content, dN,fN,fSize,fAT,fMT, fCT, fMD5) VALUES (datetime('now'),?,?,?,?,?, ?, ?, ?, ?)''', (NP, Cont, rootDir, fname, size, fatime, fmtime, fctime, fmd5))
        logging.debug(' {0:5}  {1:}'.format(xx,'fname'))
            
    db.commit()
            
    logging.info('db commitad')
   
   
    logging.info("Select")
    for row in cur.execute('''SELECT * FROM main.fileTable'''):
        print (row)

    sqlte2csv(cur) 
        
    logging.info("Slut OK före db close")    
    
    db.close()
    
    #db = sqlite3.connect(dbfile)
    #cur = db.cursor()
    
    #print ('igen')
    #for row in cur.execute("SELECT * FROM main.fileTable"):
    #   print (row)
    
    #print ('Slut')
    
    
if __name__ == '__main__':
    logging.basicConfig(level=0)
    logging.info("modulen startar som __main__ åäöÅÄÖ")
    FileListing()
    logging.info("Klart m FileListing")
    logging.shutdown()    
            
            