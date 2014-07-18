'''
Created on 2014-7-16

@author: guanxingquan
'''
from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants,MysqlConnector
from DeviceCommsAPI import DeviceServerService
import logging
import json
from arbiter.TestDeviceServerService import log

log = logging.getLogger("TestDeviceServerService")
class DeviceServerService():
    client = None 
    con = None
    def __init__(self):
        try:
            self.con = MysqlConnector.getConnection()
            self.deviceId = Config().getFormConfig(Constants.deleteDevice,"device-id")
            dsServerInfo = Mysql(self.con).getDsServerInfo(self.deviceId)
            host = dsServerInfo[0][2]
            port = dsServerInfo[0][3]
            self.client = ThriftClient.getThriftClient(host, port, DeviceServerService)
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
            num = 0
            devices = self.client.getDevices()
            for i in devices:
                log.debug('devicesId==i?')
                if i==self.deviceId:
                    num = num + 1
            if num > 0:
                log.debug('this device in DS')
            else:
                log.debug('this device not in DS')  
        except Exception,e:
            log.error('testDeviceisinDs have exception=%s',e)
            raise Exception("testDeviceisinDs exception")  
         
    
    #here are some auxiliary methods
    #frame-rate  ---  测试所得帧率
    #rated-frames --- 额定帧率
    def testDeviceFrameRate(self):
        try:
            log.debug('this test is test frame-rate==rated-frames')
            device = self.client.getDeviceInfo(self.deviceId)
            de = json.loads(device)
            fra = de["frame-rate"]
            print de["frame-rate"]
            Config().writeToConfig(Constants.frame,"frame-rate",fra)
            rate = Config().getFromConfig(Constants.frame,"rated-frames")
            percent = Config().getFromConfig(Constants.frame,"percent")
            if fra <= rate*(1+percent) and fra >= rate*(1-percent):
                log.debug('this frame-rate is true,the Device video is true')
            else:
                log.debug('this frame-rate is false')
        except Exception,e:
            log.error('testDeviceFrameRate  exception=%s',e)
            raise Exception('TestDeviceServerService.testDeviceFrameRate exception') 

if __name__ == '__main__':
    print "begin DeviceServerService test."
