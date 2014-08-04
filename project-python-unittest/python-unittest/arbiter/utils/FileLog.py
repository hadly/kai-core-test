
import logging

class GetLogger():
    
    def __init__(self,logfile):
        self.logfile = logfile
    
    def initlogger(self):
        logger = logging.getLogger()
        hdlr = logging.FileHandler(self.logfile)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.NOTSET)
        return logger