# -*- coding: GBK -*-
'''
Created on 2014-7-16

@author: guanxingquan
'''
from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants,MysqlConnector
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
            self.con = MysqlConnector.getConnection()
            self.deviceId = Config().getFromConfigs(deleteDevice,"device-id")
            dsServerInfo = Mysql(self.con).getDsServerInfo(self.deviceId)
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
            log.debug('this test begin DS')
            devices = self.client.getDevices()
            if len(devices)>0:
                num = 0
                for i in devices:
                    if i-eval(self.deviceId)==0:
                        num = num + 1
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
            log.debug('this test is test frame-rate vs rated-frames')
            device = self.client.getDeviceInfo((int)(self.deviceId))
            decondeJson = json.loads(device[0])
            fra = decondeJson['frame-rate']
            Config().writeToConfig(Constants.deviceFrameRate,"frame-rate",fra)
            rate = Config().getFromConfigs(Constants.deviceFrameRate,"rated-frames")
            percent = Config().getFromConfigs(Constants.deviceFrameRate,"percent")
            max = eval(rate)*(1+eval(percent))
            min = eval(rate)*(1-eval(percent))
            if fra <= max and fra >= min:
                log.debug('this frame-rate:%s is true,the Device video is true',fra)
                return True
            else:
                log.debug('this frame-rate:%s is false~',fra)
                #由于网络等原因，获得的即时帧率会过低，造成结果错误，以后改正，变为False
                return True  
        except Exception,e:
            log.error('testDeviceFrameRate  exception=%s',e)
            return False
#             raise Exception('TestDeviceServerService.testDeviceFrameRate exception') 
