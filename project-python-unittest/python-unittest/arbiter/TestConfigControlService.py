'''
 Created on 2014-7-16

@author: guanxingquan
'''

from CoreServices import ConfigControlService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants
from arbiter.utils.Constants import arbiter
import logging

log = logging.getLogger('testConfigControlService')
class ConfigControlServiceClient():
    client = None 
    def __init__(self):
        try:
            host = Config().getFromConfigs(arbiter, "arbiter-server-host")
            port = Config().getFromConfigs(arbiter, "config-control-server-port")
            self.client = ThriftClient.getThriftClient(host, port, ConfigControlService)
        except Exception, e:
            log.error("ConfigControlService init error:%s",e)
            raise Exception("ConfigControlService Exception")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()

    def testSetChunkSize(self):
        '''
          make sure setChunkSize() is success function
        '''
        try:
            log.debug('test setChunkSize')
            size = Config().getFromConfigs(Constants.frame,"chunk-size")
#             print size
            result = self.client.setChunkSize((int)(size))
#             print result
            if result == True:
                log.info('this function set chunk-size is success!')
            else:
                log.info('the test have error~~')
        except Exception,e:
            log.error("testSetChunkSize error:%s",e)
            raise Exception("testSetChunkSize exception")
                