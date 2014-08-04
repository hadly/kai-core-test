'''
Created on 2014-7-17

@author: guanxingquan
'''
from DeviceCommsAPI import DeviceDataReceiverService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient
from arbiter.utils.Constants import arbiter,deleteDevice,streamControl
import json
import logging
import uuid

log = logging.getLogger("TestDeviceDataReceiverService")
class DeviceDataReceiverServiceClient():
    '''
    classdocs
    '''

    client = None
    def __init__(self):
        '''
        Constructor
        '''
        try:
            host = Config().getFromConfigs(arbiter, "arbiter-server-host")
            port = Config().getFromConfigs(arbiter, "data-receiver-port")
            self.client = ThriftClient.getThriftClient(host, port, DeviceDataReceiverService)
        except Exception, e:
            log.error("DeviceManagementServer error:%s",e)
            raise Exception("DeviceDataReceiverService setup:")
        
    def tearDown(self):
        ThriftClient.closeThriftClient()
        
    def sendEventToArbiter(self):
        log.debug('the tast sendEventToArbiter start!')
        try:
           devId = Config().getFromConfigs(deleteDevice,"device-id")
           uuId = uuid.uuid1()
           Config().writeToConfig(streamControl,"event-id",str(uuId))
           stringData = {"eventId":str(uuId),"deviceId":devId,"channelId":"0"}
           sdate = json.dumps(stringData)
           istrue = self.client.sendEventData(None,None,'CAPTURE_EVENT_VIDEO',None,None,sdate,None)
           log.debug('isTrue:%s',istrue)
           if istrue:
               log.info('The process send Event to Arbiter is True') 
           else:
               log.info('The process is false')
        except Exception,e:
           log.error('The process have an error:%s',e)
           raise Exception('sendEventToArbiter Exception') 
                