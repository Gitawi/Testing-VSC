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


"""
 sys.setdefaultencoding('utf-8') Farlig function nu deletad tydligen

print ("   ".format(text.encode("utf-8")))   funkar med win-cmd chcp 852, 437 men med unicodehex (CP65001 i cmd window ger "unknown codepage" och hängning from Python)
Att "tvinga fram encoding till "utf-8" även av Unicode-strängar verkar få Python att släppa igenom print till consolen (cmd).
Om man redirectar till en Out.txt så blir det sen rätt om man öppnar i Notepad.exe
"""
CurrentWorkingDir   = "E:\Gitawi\FileListing w Python\\"
OutputDir           = CurrentWorkingDir +"slask\\"
#InputDir            = CurrentWorkingDir +'PDFer f test\\'
#InputDir           = 'D:\Dropbox\___Ark\_Konton, Löpande'
InputDir            = 'E:\OneDrive\_Shared\\191020 - Långtur'
dbfile              = OutputDir+"fillista.db"
csvOutputfile       = OutputDir+"csvOutput.csv"
SingleDir           = False # Sök endast InputDir och inte ner i trädet


logging.info("CurrentWorkingDir: " + CurrentWorkingDir)
logging.info("OutputDir: " + OutputDir)
logging.info("InputDir: " + InputDir)
logging.info("dbfile: " + dbfile)
logging.info("csvOutputfile: " + csvOutputfile)
logging.info("SingleDir: " ,  SingleDir)


        
def sqlte2csv(cur):
    if True : # With Python
        xxx = cur.execute('''SELECT * FROM main.fileTable''') # Krävs för att cur.description nedan skall initieras
        with open(csvOutputfile, 'w', newline='') as cvsfile:
            writer = csv.writer(cvsfile )
            writer.writerow([tuple[0] for tuple in cur.description]) # cur.description måste initieras med en sökning innan användning, so ovan
            writer.writerows(cur.execute('''SELECT * FROM main.fileTable''')) 

        # With SQLite
         #cur.execute('''.excel''')
         #cur.execute('''SELECT fMD5 FROM main.fileTable''')


def FileListing():
    """
    200111 - Fillistningen och placeringen av data i SQLite fungerar bra både med bara filerna ur ett directory med listOfFiles = [f for f in os.listdir(InputDir) if os.path.isfile(os.path.join(InputDir, f))]
    eller med att gå igenom hela trädet med os.path.walk()
    """

    # Initiera SQLite databas
    {db = sqlite3.connect(dbfile)
     # db = sqlite3.connect(':memory:')
     cur = db.cursor()}
    
    cur.execute('''DROP TABLE IF EXISTS main.fileTable''')
    cur.execute('''CREATE TABLE main.fileTable(stamp TEXT, NoPages INTEGER, Content TEXT,  fN TEXT, size INTEGER, fAT TEXT, fMT TEXT, fCT TEXT,  path TEXT, fBlob , fMD5 TEXT)''')
    db.commit()
    logging.info('DB skapad och klart')
    
  
       
    for path, dirs, fnames in os.walk(InputDir):
        if path != InputDir and SingleDir: break # kör inte ner i trädet
        for fname in fnames : 
            fullfname = os.path.join(path, fname)

            # Extract data from fullfname
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fullfname)
            fatime = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(atime))
            fmtime = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(mtime))
            fctime = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ctime))
            fmd5 = md5_of_file(fullfname)
            PyPDF2data = PyPDF2datafind(fullfname)
            NP = PyPDF2data[0]
            Cont = PyPDF2data[1]
            logging.debug(' {0:5}  {1:25}  {2:35} - {3:20}'.format( fullfname, atime, fatime, fmd5))
            # Enter data into SQLite
            cur.execute('''INSERT INTO main.fileTable ( stamp, NoPages, Content, fN, Size,fAT,fMT, fCT, path, fMD5) VALUES (datetime('now'),?,?,?,?,?, ?, ?, ?, ?)''', (NP, Cont, fname, size, fatime, fmtime, fctime, path, fmd5))
            #logging.debug(' {0:5}  {1:}'.format('fullfname'))
            
    db.commit()
            
    logging.info('db commitad')
   
   
    logging.info("Select")
    ## Printa till skärmen
    #for row in cur.execute('''SELECT * FROM main.fileTable'''):
    #    print (row)

    # xportera till Excelfil
    sqlte2csv(cur) 
        
    logging.info("Slut OK före db close")    
    db.commit()
    db.close()
    print ('Slut')
    

    """"
def PyPDF2datafind(fullfname):
    Hämtar text ur PDFer men är inte helt konsistent. Ibland måste pdferna "saniteras" och OCRas igen för att kunna läsas och ändå 
    kommer alla sidor inte alltid med. Dessutom är PDFerna sådana att texten kommer inte ut logiskt utan lite blandat så att man
    kan inte säkert söka på något ledord eller mening och sen hoppas på att nästa del i texten t.ex. är en faktura summa
    """

    dot = fullfname.rfind(".")
    ext = fullfname[dot:]
    txt = ""
    NP = -1
    return [NP , txt] # for testing
    if ext.upper() == ".PDF" : 
      
        # Creating a pdf file object.
        pdf = open(fullfname, "rb")
 
        # Creating pdf reader object.
            pdf_reader = PyPDF2.PdfFileReader(pdf)
 
        # Checking total number of pages in a pdf file.
        NP = pdf_reader.numPages
        for i in range(0,NP-1):
            page =          pdf_reader.getPage(i)
            txt = txt + page.extractText()
            pdf.close()
    else:
        txt = ext + " not pdf"


    return [NP , txt]
 
def md5_of_file(fullfname):
    hash_md5 = hashlib.md5()
    with open(fullfname, "rb") as f:
       for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

    
if __name__ == '__main__':
    logging.basicConfig(level=0)
    logging.info("modulen startar som __main__ åäöÅÄÖ")
    FileListing()
    logging.info("Klart m FileListing")
    logging.shutdown()    
            
            