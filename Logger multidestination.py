import logging
import time
import datetime
# Choose one SQLiteHandler by commenting
#from SQLiteHandler_amka import SQLiteHandler # Bättre tidsformat med nogrannare upplösning
from SQLiteHandler_kessler import SQLiteHandler # Mer detaljer loggas t.ex threads

# Run identification. Use as unique but identifiable filename, ad extension and path
DTName = str(datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d %H%M%S'))

"""
Logs to different destinations, individually or multidestination
"""

# Create Message Formatters to be used below with different output-handlers
# 3 alternative string formatting styles tested. I preferred '{' i.e. formatting no 1
# 1c,1f,1s a little different - to be used for different destinations = outputhandlers = handlers i.e.for console, file, SQLite db


formatter1f = logging.Formatter('{asctime}/{name}/{lineno:0=3}/{levelname:9}{message}', datefmt='%y%m%d/%H:%M:%S', style='{')
formatter1c = logging.Formatter('{asctime}/{name}/{lineno:0=3}/{levelname:9}{message}', datefmt='%H:%M:%S', style='{')
formatter1s = logging.Formatter('{name}/{lineno:0=3}/{levelname:9}{message}', datefmt='%H:%M:%S', style='{')
# create formatter with  '$'-str.Template() formatting style and add it to the handlers - not used
formatter2 = logging.Formatter('$asctime/$name/$lineno/$levelname\t$message', datefmt='%y%m%d/%H:%M:%S', style='$')
# create formatter with formatting style '%' and add it to the handlers - not used
formatter3 = logging.Formatter('%(asctime)s/%(name)s/%(lineno)d/%(levelname)s\t%(message)s', datefmt='%y%m%d/%H:%M:%S:%f')


# Initiate python logging with several "logger"s 
# file-logger
loggerf = logging.getLogger(__name__+' file')
loggerf.setLevel(logging.DEBUG)
fh = logging.FileHandler('slask\\'+DTName+".txt")
fh.setFormatter(formatter1f)
fh.setLevel(logging.DEBUG)
loggerf.addHandler(fh)

# console-logger
# gggggggg ändring
loggerc = logging.getLogger(__name__+' console')
loggerc.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(formatter1c)
ch.setLevel(logging.INFO)
loggerc.addHandler(ch)

# SQlite-logger
loggers = logging.getLogger(__name__+' sql')
loggers.setLevel(logging.DEBUG)
sq = SQLiteHandler('slask\\'+DTName+'.sqlite')
sq.setFormatter(formatter1s)
sq.setLevel(logging.DEBUG)
loggers.addHandler(sq)

# Multi-logger
loggerm = logging.getLogger(__name__+' m')
loggerm.setLevel(logging.DEBUG)
loggerm.addHandler(sq)
loggerm.addHandler(ch)
loggerm.addHandler(fh)


# Some tests
loggers.debug('Test 1 to SQL')
loggerf.warning('Some warning to File')
loggerc.error('Alarma! to Console')
loggers.debug('debug message to SQL')
loggerf.info('info message to File')
loggerc.warn('warn message to Console')
loggerm.error('error message to Multi')
loggerm.critical('critical message to Multi')

#############################################################

