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
from arbiter.utils.Constants import configControl,videoStrategy,photoStrategy
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
            deviceDetails = self.getDeviceDetails(addDevice,False)
            result = self.client.addDevice(deviceDetails)
            log.debug("add device=%s,result=%s", deviceDetails, result)
            Config().writeToConfig(updateDevice, "device-id", result)
            Config().writeToConfig(deleteDevice, "device-id", result)
            if result:
                log.debug("add device success")
                return True
            else:
                log.debug('add device to Arbiter fail')
                return False
        except Exception,e:
            log.error('Error:%s',e)
            return False
    def updateCloud(self):
        '''
           start video  
        '''
        Config().writeToConfig(addDevice, "cloud-recording-enabled","true")
        deviceDetail = self.getDeviceDetails(updateDevice,False)
        result = self.client.updateDevice(deviceDetail)
        log.debug("open the video store result : %s",result)
        return result
    
    def closeVideoRecord(self):
        Config().writeToConfig(addDevice, "cloud-recording-enabled","false")
        deviceDetail = self.getDeviceDetails(updateDevice,False)
        result = self.client.updateDevice(deviceDetail)
        log.debug("close the video store result : %s",result)
        return result
    
    def TestVideoStrategy(self):
        sum = 0
        try:
            log.debug('Test Video Strategy')
            chunk_size = Config().getFromConfigs(configControl,"chunk-size")
            result = self.updateCloud()
            if result:
                time.sleep(40)
            istrue = True
            while istrue:
                time_mrt = time.time()
                births = time.localtime(time_mrt)
                datess = time.strftime("%d%m%Y%H%M%S",time.gmtime(time_mrt))
                timess = time.strftime("%d%m%Y%H%M%S",births)
                tim_mins = time.strftime("%M",births)
                tim_sec = time.strftime('%S',births)
                if eval(tim_mins)%(int)(chunk_size)==0 and tim_sec=="00":
                    if sum==0:
                        Config().writeToConfig(videoStrategy, "liveview-begin-time-UTC",datess)
                        Config().writeToConfig(videoStrategy, "liveview-begin-time-local",timess)
                    log.debug('msg:the next will sleep 2*60*3s~')
                    if sum!=0:
                        Config().writeToConfig(addDevice, "cloud-recording-enabled","true")
                        self.client.updateDevice(self.getDeviceDetails(updateDevice,False))
                    sum = sum + 1
                    time.sleep(eval(chunk_size)*60*2)
                    Config().writeToConfig(addDevice, "cloud-recording-enabled","false")
                    deviceDetail2 = self.getDeviceDetails(updateDevice,False)
                    self.client.updateDevice(deviceDetail2)
                    if sum == 2:
                        Config().writeToConfig(videoStrategy, "liveview-end-time-UTC",time.strftime("%d%m%Y%H%M%S",time.gmtime()))
                        Config().writeToConfig(videoStrategy, "liveview-end-time-local",time.strftime("%d%m%Y%H%M%S",time.localtime()))
                        istrue = False
                    if sum == 1:
                        time.sleep(eval(chunk_size)*30)
                    log.debug('the %d cycle end',sum)
            log.debug('TestVideoStrategy success!')
            return True
        except Exception,e:
            log.error('error:%s',e)
            log.debug('The Test Strategy start fail')
            return False
     
    def testPhotoStrategy(self):
        sum = 0
        try:
            log.debug('Test Image Strategy')
            interval = Config().getFromConfigs(addDevice,"snapshot-recording-interval")
            Config().writeToConfig(addDevice, "snapshot-recording-enabled","true")
            deviceDetail1 = self.getDeviceDetails(updateDevice,False)
            result = self.client.updateDevice(deviceDetail1)
            log.debug('result:%s',result)
            if result and sum==0:
                time.sleep(40)
            istrue = True
            while istrue:
                timess = time.time()
                tim_sec = time.strftime('%S',time.localtime(timess))
                if eval(str(timess))%eval(interval)==0 and eval(str(tim_sec))%eval(interval)==0:
                    if sum==0:
                        Config().writeToConfig(photoStrategy, "photo-begin-time-local",time.strftime("%d%m%Y%H%M%S",time.localtime(timess)))
                        Config().writeToConfig(photoStrategy, "photo-begin-time-UTC",time.strftime("%d%m%Y%H%M%S",time.gmtime(timess)))
                    if sum!=0:
                        Config().writeToConfig(addDevice, "snapshot-recording-enabled","true")
                        self.client.updateDevice(self.getDeviceDetails(updateDevice,False))
                    sum = sum + 1
                    log.debug('msg:sleep 60s')
                    time.sleep(eval(interval)*12)
                    Config().writeToConfig(addDevice, "snapshot-recording-enabled","false")
                    deviceDetail2 = self.getDeviceDetails(updateDevice,False)
                    result = self.client.updateDevice(deviceDetail2)
                    if result==True and sum==1:
                        log.debug('msg:sleep 60s')
                        time.sleep(eval(interval)*12)
                        log.debug('waiting  next~')
                    if sum == 2:
                        Config().writeToConfig(photoStrategy, "photo-end-time-UTC",time.strftime("%d%m%Y%H%M%S",time.gmtime()))
                        Config().writeToConfig(photoStrategy, "photo-end-time-local",time.strftime("%d%m%Y%H%M%S",time.localtime()))
                        istrue = False
            log.debug('testPhotoStrategy success!')
            return True
        except Exception,e:
            log.error('error:%s',e)
            log.debug('Test Strategy start fail')
            return False
    
    def testDeleteDevice(self):
        try:
            log.debug("test delete device")
            deviceId = Config().getFromConfigs(deleteDevice, "device-id")
            result = self.client.deleteDevice(deviceId)
            log.debug("remove device=" + deviceId + ",result=" + (str)(result))            
            if result == False:
                log.debug('delete device fail')
            log.debug("delete device success")
            return result
        except Exception,e:
            log.error("delete device exception=%s", e)
            raise Exception("delete device exception")
         
    def testUpdateDevice(self):
        try:
            log.debug("test update device")
            deviceDetails = self.getDeviceDetails(updateDevice,True)
            result = self.client.updateDevice(deviceDetails)
            log.debug("update device=%s,result=%s", deviceDetails, result)
            if result == False:
                log.debug('update device fail')
#                 raise Exception("update device fail")
            log.debug("update device success")
            return result
        except Exception,e:
            log.error("update exception, %s", e)
            raise Exception("update device fail")
    
    
    
    #here are some auxiliary methods
    def getDeviceDetails(self, manipulate,ishost):
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
            deviceId = config.get(updateDevice,'device-id')
            if ishost==True:
                host = config.get(updateDevice,'host')
            else:
                host = config.get(addDevice,'host')
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
