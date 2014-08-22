# -*- coding: GBK -*-
'''
Created on 2014-7-16

@author: guanxingquan
'''
from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants
from DeviceCommsAPI import DeviceServerService
from arbiter.utils.Constants import deleteDevice
import logging
import json
from lib2to3.fixer_util import String
log = logging.getLogger("TestDeviceServerService")
class DeviceServerServiceClient():
    client = None 
    con = None
    def __init__(self):
        try:
            log.debug('************DeviceServerServiceClient init come in*******************')
            self.deviceId = Config().getFromConfigs(deleteDevice,"device-id")
            dsServerInfo = Mysql().getDsServerInfo(self.deviceId)
            if len(dsServerInfo)!=0:
                host = dsServerInfo[0][2]
#                 print host
                port = dsServerInfo[0][3]
#                 print port
                self.client = ThriftClient.getThriftClient(host, port, DeviceServerService)
#                 print self.client
            log.debug('************DeviceServerServiceClient init End*******************')
        except Exception, e:
            log.error("DeviceServerService setup:%s",e)
            raise Exception("DeviceServerService setup error")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
    
    def testDeviceisinDs(self):
        '''
          make sure this deviceId in DS
        '''
        try:
            log.debug(self.client)
            devices = self.client.getDevices()
            log.debug(len(devices))
            if len(devices)>0:
                num = 0
                for i in devices:
                    if i-eval(self.deviceId)==0:
                        num = num + 1
                log.debug('the device number in DS : %d',num)
                
                if num > 0:
                    log.debug('this device in DS')
                    return True
                else:
                    log.debug('this device not in DS')
                    return False  
        except Exception,e:
            log.error('testDeviceisinDs have exception=%s',e)
            return False
         
    
    #here are some auxiliary methods
    #frame-rate  ---  
    #rated-frames --- 
    def testDeviceFrameRate(self):
        try:
            log.debug('this test is test frame_rate_in_ds vs rated-frames')
            device = self.client.getDeviceInfo((int)(self.deviceId))
            decondeJson = json.loads(device[0])
            frame_rate_in_ds = decondeJson['frame-rate']
            Config().writeToConfig(Constants.deviceFrameRate,"frame-rate",frame_rate_in_ds)
            rated_frames = Config().getFromConfigs(Constants.deviceFrameRate,"rated-frames")
            percent = Config().getFromConfigs(Constants.deviceFrameRate,"max-percent")
            max = eval(rated_frames)*(1+eval(percent))
            min = eval(rated_frames)*(1-eval(percent))
            if frame_rate_in_ds <= max and frame_rate_in_ds >= min:
                log.debug('this frame-rate:%s is true,the Device video is true',frame_rate_in_ds)
                return True
            else:
                log.debug('this frame-rate:%s is false~',frame_rate_in_ds)
                log.info("the frame rate from DS is %s, expected rate is %s, something is wrong. False",frame_rate_in_ds,rated_frames)
                return False  
        except Exception,e:
            log.error('testDeviceFrameRate  exception=%s',e)
            return False
#             raise Exception('TestDeviceServerService.testDeviceFrameRate exception') 
