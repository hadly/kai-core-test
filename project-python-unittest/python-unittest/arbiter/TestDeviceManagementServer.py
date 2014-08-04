# -*- coding: GBK -*-
'''
Created on 2014-6-18

@author: lizhinian
'''

from CoreServices import DeviceManagementService
from arbiter.utils.ConfigurationReader import Config
from CoreServices.ttypes import DeviceDetails
from arbiter.utils import ThriftClient
from arbiter.utils.Constants import arbiter
from arbiter.utils.Constants import addDevice
from arbiter.utils.Constants import updateDevice
from arbiter.utils.Constants import deleteDevice
from arbiter.utils.Constants import frame
from arbiter.utils.Constants import streamControl
import logging
import time
#log = logging.getLogger("TestDeviceManagementServer")
log = logging.getLogger("TestDeviceManagementServer")
class DeviceManagementServer():
    client = None 
    def __init__(self):
        try:
            host = Config().getFromConfigs(arbiter, "arbiter-server-host")
            port = Config().getFromConfigs(arbiter, "device-management-server-port")
            self.client = ThriftClient.getThriftClient(host, port, DeviceManagementService)
        except Exception,e:
            log.error("DeviceManagementServer error:%s",e)
            raise Exception("DeviceManagementServer setup!")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
    
    def testAddDevice(self):
        try:
            log.debug("test add device")
            deviceDetails = self.getDeviceDetails(addDevice)
            result = self.client.addDevice(deviceDetails)
            log.debug("add device=%s,result=%s", deviceDetails, result)
            #将得到的deviceId写到要更新和删除的配置文件
            Config().writeToConfig(updateDevice, "device-id", result)
            Config().writeToConfig(deleteDevice, "device-id", result)
            if result == False:
                log.info('add device to Arbiter fail')
                raise Exception("add device to Arbiter fail")
            log.info("add device success")
        except :
            raise Exception("add device to Arbiter fail")
    
    def TestVideoStrategy(self):
        sum = 0
        try:
            log.debug('The Test Strategy')
            chunk_size = Config().getFromConfigs(frame,"chunk-size")
            Config().writeToConfig(addDevice, "cloud-recording-enabled","true")
            deviceDetail1 = self.getDeviceDetails(updateDevice)
#             print deviceDetail1
            result = self.client.updateDevice(deviceDetail1)
            if result and sum==0:
                time.sleep(40)
            #开启时间监控~
            istrue = True
            while istrue:
                time_mrt = time.time()
                births = time.localtime(time_mrt)
#                 print "1"
                datess = time.strftime("%d%m%Y%H%M%S",time.gmtime(time_mrt))
                timess = time.strftime("%d%m%Y%H%M%S",births)
#                 print "2"
                tim_mins = time.strftime("%M",births)
#                 print "3"
                tim_sec = time.strftime('%S',births)
#                 print '4'
#                 log.debug('msg:sssssssssss') 
                if eval(tim_mins)%(int)(chunk_size)==0 and tim_sec=="00":
                    if sum==0:
                        Config().writeToConfig(streamControl, "liveview-begin-time",datess)#记录开始时间
                        Config().writeToConfig(frame, "liveview-begin-time-eight",timess)
                    #开启存储
                    log.debug('msg:the next will sleep 2*60*3s~')
                    if sum!=0:
                        Config().writeToConfig(addDevice, "cloud-recording-enabled","true")
                        self.client.updateDevice(self.getDeviceDetails(updateDevice))
                    sum = sum + 1
                    time.sleep(eval(chunk_size)*60*2)
                    Config().writeToConfig(addDevice, "cloud-recording-enabled","false")
                    deviceDetail2 = self.getDeviceDetails(updateDevice)
                    self.client.updateDevice(deviceDetail2)
                    if sum == 2:
                        Config().writeToConfig(streamControl, "liveview-end-time",time.strftime("%d%m%Y%H%M%S",time.gmtime()))#记录结束时间
                        Config().writeToConfig(frame, "liveview-end-time-eight",time.strftime("%d%m%Y%H%M%S",time.localtime()))
                        istrue = False
                    time.sleep(eval(chunk_size)*30)
                    log.debug('msg:one cycle end time')
            log.info('TestVideoStrategy success!')
        except Exception,e:
            log.debug('msg:%s',e)
            raise Exception("The Test Strategy start fail")
    
    def testPhotoStrategy(self):
        sum = 0
        try:
            log.debug('The Test Strategy')
            interval = Config().getFromConfigs(addDevice,"snapshot-recording-interval")
            Config().writeToConfig(addDevice, "snapshot-recording-enabled","true")
            deviceDetail1 = self.getDeviceDetails(updateDevice)
#             print deviceDetail1
            result = self.client.updateDevice(deviceDetail1)
            log.debug('result:%s',result)
            #开启时间监控~
            if result and sum==0:
                time.sleep(40)
            istrue = True
            while istrue:
                timess = time.time()
                tim_sec = time.strftime('%S',time.localtime(timess))
                if eval(str(timess))%eval(interval)==0:
                    if sum==0:
                        Config().writeToConfig(frame, "photo-begin-time-eight",time.strftime("%d%m%Y%H%M%S",time.localtime(timess)))
                        Config().writeToConfig(frame, "photo-begin-time",time.strftime("%d%m%Y%H%M%S",time.gmtime(timess)))#记录开始时间
                    if sum!=0:
                        Config().writeToConfig(addDevice, "snapshot-recording-enabled","true")
                        self.client.updateDevice(self.getDeviceDetails(updateDevice))
                    sum = sum + 1
                    log.debug('msg:sleep 60s')
                    time.sleep(eval(interval)*12)#等待60s后停止存储照片
                    Config().writeToConfig(addDevice, "snapshot-recording-enabled","false")
                    deviceDetail2 = self.getDeviceDetails(updateDevice)
                    result = self.client.updateDevice(deviceDetail2)
                    if result==True and sum==1:
                        log.debug('msg:sleep 60s')
                        time.sleep(eval(interval)*12)#等待60s后再次循环，重复：存储——等待——停止
                        log.debug('waiting  next~')
                    if sum == 2:
                        Config().writeToConfig(frame, "photo-end-time",time.strftime("%d%m%Y%H%M%S",time.gmtime()))#记录结束时间
                        Config().writeToConfig(frame, "photo-end-time-eight",time.strftime("%d%m%Y%H%M%S",time.localtime()))
                        istrue = False
            log.info('testPhotoStrategy success!')
        except Exception,e:
            log.error('error:%s',e)
            raise Exception("The Test Strategy start fail")
    
    def testDeleteDevice(self):
        try:
            log.debug("test delete device")
            deviceId = Config().getFromConfigs(deleteDevice, "device-id")
            result = self.client.deleteDevice(deviceId)
            log.debug("remove device=" + deviceId + ",result=" + (str)(result))            
            if result == False:
                log.info('delete device fail')
                raise Exception("delete device fail")
            log.info("delete device success")
        except Exception,e:
            log.error("delete device exception=%s", e)
            raise Exception("delete device exception")
         
    def testUpdateDevice(self):
        try:
            log.debug("test update device")
            deviceDetails = self.getDeviceDetails(updateDevice)
            result = self.client.updateDevice(deviceDetails)
            log.debug("update device=%s,result=%s", deviceDetails, result)
            if result == False:
                log.info('update device fail')
                raise Exception("update device fail")
            log.info("update device success")
        except Exception,e:
            log.error("update exception, %s", e)
            raise Exception("update device fail")
    
    
    
    #here are some auxiliary methods
    def getDeviceDetails(self, manipulate):
        configuration = Config()
        config = configuration.getConfig()
        if manipulate == addDevice:
            deviceId = config.get(addDevice,'device-id')
            name = config.get(addDevice,'name')
            key = config.get(addDevice,'key')
            host = config.get(addDevice,'host')
            port = config.get(addDevice,'port')
            login = config.get(addDevice,'login')
            password = config.get(addDevice,'password')
            address = config.get(addDevice,'address')
            lat = config.get(addDevice,'lat')
            lng = config.get(addDevice,'lng')
            accountId = config.get(addDevice,'account-id')
            modelId = config.get(addDevice,'model-id')
            statusId = None
            functionalityId = None
            alertFlag = None
            alive = None
            currentPositionId = None
            action = None
            eventSettings = None
            deviceServerUrls = config.get(addDevice,'device-server-urls')
            liveview = None
            snapshotRecordingEnabled = config.get(addDevice,'snapshot-recording-enabled')
            snapshotRecordingInterval = config.get(addDevice,'snapshot-recording-interval')
            cloudRecordingEnabled = config.get(addDevice,'cloud-recording-enabled')
            device = DeviceDetails(deviceId, name, key, host, port, login, 
                               password, address, lat, lng, accountId,
                               modelId, statusId , functionalityId , alertFlag ,
                                alive , currentPositionId , action , eventSettings ,
                                 deviceServerUrls, liveview , snapshotRecordingEnabled, 
                                 snapshotRecordingInterval, cloudRecordingEnabled)
            return device
        elif manipulate == updateDevice:
            #更新时只有deviceId和host从updateDevice的section读取,别的都从addDevice的section读取
            deviceId = config.get(updateDevice,'device-id')
            host = config.get(updateDevice,'host')
            
            name = config.get(addDevice,'name')
            key = config.get(addDevice,'key')
            port = config.get(addDevice,'port')
            login = config.get(addDevice,'login')
            password = config.get(addDevice,'password')
            address = config.get(addDevice,'address')
            lat = config.get(addDevice,'lat')
            lng = config.get(addDevice,'lng')
            accountId = config.get(addDevice,'account-id')
            modelId = config.get(addDevice,'model-id')
            statusId = None
            functionalityId = None
            alertFlag = None
            alive = None
            currentPositionId = None
            action = None
            eventSettings = None
            deviceServerUrls = config.get(addDevice,'device-server-urls')
            liveview = None
            snapshotRecordingEnabled = config.get(addDevice,'snapshot-recording-enabled')
            snapshotRecordingInterval = config.get(addDevice,'snapshot-recording-interval')
            cloudRecordingEnabled = config.get(addDevice,'cloud-recording-enabled')
            device = DeviceDetails(deviceId, name, key, host, port, login, 
                               password, address, lat, lng, accountId,
                               modelId, statusId , functionalityId , alertFlag ,
                                alive , currentPositionId , action , eventSettings ,
                                 deviceServerUrls, liveview , snapshotRecordingEnabled, 
                                 snapshotRecordingInterval, cloudRecordingEnabled)
            return device
        else:
            log.debug("no manipulate selected")
            return

 
if __name__ == '__main__':
    log.debug("begin DeviceManagementServer test.")
    DeviceManagementServer().testAddDevice()



