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
#             print self.client
            devices = self.client.getDevices()
#             print len(devices)     
#             print "devices", devices       
            if len(devices)>0:
                num = 0
                for i in devices:
                    if i-eval(self.deviceId)==0:
                        num = num + 1
                if num > 0:
                    log.info('this device in DS')
                else:
                    log.info('this device not in DS')  
        except Exception,e:
            log.error('testDeviceisinDs have exception=%s',e)
            raise Exception("testDeviceisinDs exception")  
         
    
    #here are some auxiliary methods
    #frame-rate  ---  
    #rated-frames --- 
    def testDeviceFrameRate(self):
        try:
            log.debug('this test is test frame-rate vs rated-frames')
            device = self.client.getDeviceInfo((int)(self.deviceId))
#             print device[0]
#             de = json.loads(json.dumps(device[0]))
#             print type(de)
#             print len(de)
#             print de
#             print de[0]['frame-rate']
#             fra = (float)(de[0]['frame-rate'])
            decondeJson = json.loads(device[0])
#             print "list=", decondeJson['frame-rate']
#             print "frame-rate=", decondeJson[0]['frame-rate']
            fra = decondeJson['frame-rate']
#             print fra
            Config().writeToConfig(Constants.frame,"frame-rate",fra)
            rate = Config().getFromConfigs(Constants.frame,"rated-frames")
#             print rate
            percent = Config().getFromConfigs(Constants.frame,"percent")
#             print percent
            max = eval(rate)*(1+eval(percent))
            min = eval(rate)*(1-eval(percent))
#             print max
#             print min
            if fra <= max and fra >= min:
                log.info('this frame-rate:%s is true,the Device video is true',fra)
            else:
                log.info('this frame-rate:%s is false~',fra)
        except Exception,e:
            log.error('testDeviceFrameRate  exception=%s',e)
            raise Exception('TestDeviceServerService.testDeviceFrameRate exception') 
