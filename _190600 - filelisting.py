# -*- coding: utf-8 -*-
#!/usr/bin/env python


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
""""
 sys.setdefaultencoding('utf-8') Farlig function nu deletad tydligen

print ("   ".format(text.encode("utf-8")))   funkar med win-cmd chcp 852, 437 men med unicodehex (CP65001 i cmd window ger "unknown codepage" och hängning from Python)
Att "tvinga fram encoding till "utf-8" även av Unicode-strängar verkar få Python att släppa igenom print till consolen (cmd).
Om man redirectar till en Out.txt så blir det sen rätt om man öppnar i Notepad.exe
"""
slask = "slask\\"
dbfile = slask+"fillista.db"
csvOutput = slask+"csvOutput.csv"


#MD5_finns = hashlib.algorithms_guaranteed

#def md5_for_file(f, block_size=2**20):
    #md5 = hashlib.md5()
    #while True:
    #    data = f.read(block_size)
    #    if not data:
    #        break
    #    md5.update(data)
    #return md5.digest()

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
    
     # Initiera databas  
     db = sqlite3.connect(dbfile)
     #db = sqlite3.connect(':memory:')
     cur = db.cursor()
    
     cur.execute('''DROP TABLE IF EXISTS main.fileTable''')
     cur.execute('''CREATE TABLE main.fileTable(stamp TEXT, fN TEXT, fS INTEGER, fAT TEXT, fMT INTEGER, fCT TEXT, fSize INTEGER, dN TEXT, fDTime TEXT, fMD5 TEXT)''')
     db.commit()
     logging.info('DB skapad och klart')
    
    
    
     # Set the directory to fetch fillist from

     rootDir = 'PDFer f test'
     #rootDir = 'D:\Dropbox\___Ark\_Kvitton'
     logging.info("rootdir: " + rootDir)
    
    
     xx=0
     for dirName, subdirList, fileList in os.walk(rootDir):
         xx = xx + 1
    


         for fname in fileList:
             xx = xx+1
             # md5_for_file(f, block_size=2**20)
             path = os.path.join(dirName, fname)
             (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
             fatime = time.strftime('%Y%m%d %H:%M:%S',time.gmtime(atime))
             fmtime = time.strftime('%Y%m%d %H:%M:%S',time.gmtime(mtime))
             fctime = time.strftime('%Y%m%d %H:%M:%S',time.gmtime(ctime))
             fmd5 = md5_of_file(path)
             logging.debug(' {0:5}  {1:25}  {2:35} - {3:20}'.format( xx, fname, atime, fatime, fmd5))
             cur.execute('''INSERT INTO main.fileTable (stamp,dN,fN,fSize,fAT,fMT, fCT, fMD5) VALUES (datetime('now'),?,?,?, ?, ?, ?, ?)''', (dirName, fname, size, fatime, fmtime, fctime, fmd5))
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
            
            