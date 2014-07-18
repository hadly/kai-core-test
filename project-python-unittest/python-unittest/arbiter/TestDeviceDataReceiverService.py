'''
Created on 2014-7-17

@author: guanxingquan
'''
from DeviceCommsAPI import DeviceDataReceiverService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient
from arbiter.utils.Constants import arbiter,deleteDevice
import json
import logging
from arbiter.TestDeviceDataReceiverService import log

log = logging.getLogger("TestDeviceDataReceiverService")
class DeviceDataReceiverService():
    '''
    classdocs
    '''

    client = None
    def __init__(self):
        '''
        Constructor
        '''
        try:
            host = Config().getFromConfig(arbiter, "arbiter-server-host")
            port = Config().getFromConfig(arbiter, "device-management-server-port")
            self.client = ThriftClient.getThriftClient(host, port, DeviceDataReceiverService)
        except Exception, e:
            log.error("DeviceManagementServer setup:%s",e)
            raise Exception("DeviceDataReceiverService setup:")
        
    def tearDown(self):
        ThriftClient.closeThriftClient()
        
    def sendEventToArbiter(self):
        try:
           devId = Config().getFromConfig(deleteDevice,"device-id")
           stringData = {eventId:'95754ca2-4037-4747-ab38',deviceId:devId,channelId:0}
           sdate = json.dump(stringData)
           istrue = self.client.sendEventData(None,devId,'CAPTURE_EVENT_VIDEO',None,None,sdate,None)
           if istrue:
               log.debug('The process send Event to Arbiter is True') 
           else:
               log.debug('The process is false')
        except Exception,e:
           log.error('The process have an error:%s',e)
           raise Exception('sendEventToArbiter Exception') 
                