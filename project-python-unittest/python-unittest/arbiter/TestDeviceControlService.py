# -*- coding:GBK -*-
'''
Created on 2014-8-18

@author: guanxingquan
'''
from CoreServices import DeviceControlService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants
from arbiter.utils.Constants import arbiter,deleteDevice
import logging
log = logging.getLogger('testDeviceControlService')
class DeviceControlServiceClient():
    client = None
    def __init__(self):
        try:
            host = Config().getFromConfigs(arbiter,"arbiter-server-host")
            port = Config().getFromConfigs(arbiter,"device-control-port")
            self.client = ThriftClient.getThriftClient(host,port,DeviceControlService)
        except Exception,e:
            log.error("Error:%s",e)
            raise Exception("DeviceControlService _init_ Exception")
        
    def judgeDeviceStatus(self):
        try:
            deviceId = Config().getFromConfigs(deleteDevice,"device-id")
            result = self.client.getDeviceStatus(deviceId)
            return result
        except Exception,e:
            log.error("Error:%s",e)
        