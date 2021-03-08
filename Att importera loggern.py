from datetime import datetime
#Python_Logging/loggsetup.py
import sys
sys.path.append('E:\Gitawi\Python_Logging')
print(sys.path)
from Loggerdef import loggsetup

#from .Python_Logging.loggerdef import loggsetup


def TestarLoggern():
    RunID = str(datetime.now().strftime('%y%m%d %H%M%S.%f'))
    print(RunID)
    # RunID = "RunID"
    # RunID = str(datetime.fromtimestamp(datetime.now()).strftime('%y%m%d %H%M%S'))
    AppID = "Python App Test"
    logger = loggsetup(RunID, AppID,("file","sql","cons"))
   
    
    logger.debug('Debug kommentar')
    logger.info('Kommentar från info')
    logger.error('Real Error')

    return


print("Hello World")
TestarLoggern()
