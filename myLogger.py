import logging
from config import *
import sys


class LOG():

    _LOG = None  # class variable

    def __init__(self, print_to_console=True):
        self.LOG = logging.getLogger('POS')
        # stdout also
        if print_to_console:
            hdlr = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')  
            hdlr.setFormatter(formatter)
            self.LOG.addHandler(hdlr)
        hdlr = logging.FileHandler(LOGFILENAME)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')  
        hdlr.setFormatter(formatter)
        self.LOG.addHandler(hdlr)

        levelmap = {"DEBUG":logging.DEBUG,"INFO":logging.INFO,
                    "WARNING":logging.WARNING,"ERROR":logging.ERROR
                    }
        if LOGLEVEL in levelmap:
            l_level = levelmap[LOGLEVEL]
        else:
            l_level = logging.INFO
        self.LOG.setLevel(l_level)
        
    @staticmethod
    def debug(s):
        if LOG._LOG is None:
            o = LOG()
            LOG._LOG = o.LOG
        LOG._LOG.debug(s[:200])

    @staticmethod
    def info(s):
        if LOG._LOG is None:
            o = LOG()
            LOG._LOG = o.LOG
        LOG._LOG.info(s)
        
    @staticmethod
    def warning(s):
        if LOG._LOG is None:
            o = LOG()
            LOG._LOG = o.LOG
        LOG._LOG.warning(s)

    @staticmethod
    def error(s):
        if LOG._LOG is None:
            o = LOG()
            LOG._LOG = o.LOG
        LOG._LOG.error(s)
