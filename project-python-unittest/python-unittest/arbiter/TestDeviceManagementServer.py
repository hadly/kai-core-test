# -*- coding: GBK -*-
'''
Created on 2014-6-18

@author: lizhinian
'''

from CoreServices import DeviceManagementService
from arbiter.utils.ConfigurationReader import Config
from CoreServices.ttypes import DeviceDetails
from arbiter.utils import ThriftClient, LogUtil
from arbiter.utils.Constants import arbiter
from arbiter.utils.Constants import addDevice
from arbiter.utils.Constants import updateDevice
from arbiter.utils.Constants import deleteDevice

#log = logging.getLogger("TestDeviceManagementServer")
log = LogUtil.getLog("TestDeviceManagementServer")
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



