'''
 Created on 2014-7-16

@author: guanxingquan
'''

from CoreServices import ConfigControlService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants
from arbiter.utils.Constants import arbiter
import logging
from arbiter.TestConfigControlService import log

log = logging.getLogger('testConfigControlService')
class ConfigControlService():
    client = None 
    def __init__(self):
        try:
            host = Config().getFromConfig(arbiter, "arbiter-server-host")
            port = Config().getFromConfig(arbiter, "device-management-server-port")
            self.client = ThriftClient.getThriftClient(host, port, ConfigControlService)
        except Exception, e:
            log.error("ConfigControlService setup:%s",e)
            raise Exception("ConfigControlService setup:")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()

    def testSetChunkSize(self):
        '''
          make sure setChunkSize() is success function
        '''
        try:
            log.debug('test setChunkSize')
            size = Config().getFromConfig(Constants.frame,"chunk-size")
            result = self.client.setChunkSize(size)
            if result == True:
                log.debug('this function set chunk-size is success!')
            else:
                log.debug('the test have error~~')
        except Exception,e:
            log.error("testSetChunkSize exception:%s",e)
            raise Exception("testSetChunkSize exception")
                