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
from arbiter.TestDeviceManagementServer import log
#log = logging.getLogger("TestDeviceManagementServer")
log = logging.getLogger("TestDeviceManagementServer")
class DeviceManagementServer():
    client = None 
    def __init__(self):
        try:
            host = Config().getFromConfig(arbiter, "arbiter-server-host")
            port = Config().getFromConfig(arbiter, "device-management-server-port")
            self.client = ThriftClient.getThriftClient(host, port, DeviceManagementService)
        except Exception, e:
            log.error("DeviceManagementServer setup:%s",e)
            raise Exception("DeviceManagementServer setup:")
    
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
                raise Exception("add device to Arbiter fail")
            log.debug("add device success")
        except :
            raise Exception("add device to Arbiter fail")
    
    def TestVideoStrategy(self):
        sum = 0
        try:
            log.debug('The Test Strategy')
            chunk_size = Config().getFromConfig(frame,"chunk-size")
            Config().writeToConfig(addDevice, "cloud-recording-enabled",1)
            deviceDetail1 = self.getDeviceDetails(updateDevice)
            #开启时间监控~
            istrue = True
            while istrue:
                births = time.localtime(time.time())
                datess = time.strftime("%d%m%Y%H%M%S",births)
                tim_mins = time.strftime("%M",births)
                tim_sec = time.strftime('%S',births)
                if eval(tim_mins%chunk_size)==0 and tim_sec=="00":
                    if sum==0:
                        Config().writeToConfig(streamControl, "liveview-begin-time",datess)#记录开始时间
                    #开启存储
                    result = self.client.updateDevice(deviceDetail1)
                    sum = sum + 1
                    time.sleep(eval(chunk_size)*60*2)
                    Config().writeToConfig(addDevice, "cloud-recording-enabled",0)
                    deviceDetail2 = self.getDeviceDetails(updateDevice)
                    self.client.updateDevice(deviceDetail2)
                    if sum == 2:
                        Config().writeToConfig(streamControl, "liveview-end-time",time.strftime("%d%m%Y%H%M%S",time.localtime(time.time())))#记录结束时间
                        istrue = False
                    time.sleep(eval(chunk_size)*60*1)
        except :
            raise Exception("The Test Strategy start fail")
    
    def testPhotoStrategy(self):
        sum = 0
        try:
            log.debug('The Test Strategy')
            interval = Config().getFromConfig(addDevice,"snapshot-recording-interval")
            Config().writeToConfig(addDevice, "snapshot-recording-enabled",1)
            deviceDetail1 = self.getDeviceDetails(updateDevice)
            #开启时间监控~
            istrue = True
            while istrue:
                births = time.localtime(time.time())
                datess = time.strftime("%d%m%Y%H%M%S",births)
                tim_sec = time.strftime('%S',births)
                if eval(tim_sec%interval)==0:
                    if sum==0:
                        Config().writeToConfig(frame, "photo-begin-time",datess)#记录开始时间
                    #开启存储
                    result = self.client.updateDevice(deviceDetail1)
                    sum = sum + 1
                    time.sleep(eval(interval)*6)#等待30s后停止存储照片
                    Config().writeToConfig(addDevice, "snapshot-recording-enabled",0)
                    deviceDetail2 = self.getDeviceDetails(updateDevice)
                    self.client.updateDevice(deviceDetail2)
                    time.sleep(eval(interval)*4)#等待20s后再次循环，重复：存储——等待——停止
                    if sum == 2:
                        Config().writeToConfig(frame, "photo-end-time",time.strftime("%d%m%Y%H%M%S",time.localtime(time.time())))#记录结束时间
                        istrue = False
        except :
            raise Exception("The Test Strategy start fail")
    
    def testDeleteDevice(self):
        try:
            log.debug("test delete device")
            deviceId = Config().getFromConfig(deleteDevice, "device-id")
            result = self.client.deleteDevice(deviceId)
            log.debug("remove device=" + deviceId + ",result=" + (str)(result))            
            if result == False:
                raise Exception("delete device fail")
            log.debug("delete device success")
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
                raise Exception("update device fail")
            log.debug("update device success")
        except Exception,e:
            log.debug("update exception, %s", e)
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



