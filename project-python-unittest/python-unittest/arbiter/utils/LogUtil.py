# -*- coding: GBK -*-
'''
Created on 2014-6-23

@author: Administrator
'''
import logging

logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s] %(filename)s(%(funcName)s:%(lineno)d)[%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='python-unittest.log',
                filemode='w')

#################################################################################################
#����һ��StreamHandler����INFO�������ߵ���־��Ϣ��ӡ����׼���󣬲�������ӵ���ǰ����־�������#
console = logging.StreamHandler()
console.setLevel(logging.NOTSET)
formatter = logging.Formatter('[%(asctime)s] %(filename)s(%(funcName)s:%(lineno)d)[%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################

def getLog(logger):
    return logging.getLogger(logger)

def debug(msg):
    logging.debug(msg)
    
def info(msg):
    logging.info(msg)
    
def error(msg):
    logging.error(msg)    

if __name__ == '__main__':
    debug("nihao")