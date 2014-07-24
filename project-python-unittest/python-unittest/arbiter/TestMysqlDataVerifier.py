'''
Created on 2014-6-20

@author: Administrator
'''
#you should check the data in MySQL to verify if your Operation
#is successful in this Class

from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils import MysqlConnector, Constants
from arbiter.utils.Constants import addedDeviceName
from arbiter.utils.ConfigurationReader import Config
import time
import logging

log = logging.getLogger("TestMysqlDataVerifier")
class MysqlDataVerifier():
    
    con = None
    def __init__(self):
        #connect to DB
        self.con = MysqlConnector.getConnection()
        
    def tearDown(self):
        #close DB connection
        MysqlConnector.closeConnection()
        
    def testCorrectnessInDevices(self):
        '''
        check if there is a device named "unittest-amtk" in devices
        '''
        try:
            log.debug("test if device added to table devices")
            #select from devices to verify if there is a device named "unittest-amtk"
            device = Mysql(self.con).getDevice()
            log.debug("devices=%s", device)
            #the second one is device name
            deviceName = device[0][1]
            log.debug("device name in devices=" + deviceName)
            if deviceName != addedDeviceName:
                raise Exception("maybe device added fail")
            log.debug("added to devices correctly")
        except Exception,e:
            log.error("exception, %s", e)
            raise Exception("maybe device added fail")
    
    def testCorrectnessInDsDeviceInfo(self):
        '''
        check if there is a device named "unittest-amtk" in ds_device_info
        '''
        try:
            log.debug("test if device added to ds_device_info")
            #get device's id whose name is "unittest-amtk" 
            device = Mysql(self.con).getDevice()
            deviceId = device[0][0]#the first filed in devices is deviceId
            
            #select from ds_device_info to verify if there is a device named "unittest-amtk"        
            dsDeviceInfo = Mysql(self.con).getDsDeviceInfo(deviceId)
            log.debug("ds_device_info=%s", dsDeviceInfo)
            #the second one is device_info which contains deviceName
            deviceInfo = dsDeviceInfo[0][2]
            isDeviceExist = False
            if addedDeviceName in deviceInfo:
                isDeviceExist = True
            log.debug("device name in ds_device_info=%s",deviceInfo)
            if isDeviceExist != True:
                raise Exception("maybe ds_device_info added fail")
            log.debug("added to dsDeviceInfo correctly")
        except Exception,e:
            log.error("exception, %s", e)
            raise Exception("maybe ds_device_info added fail")
    
    def testIfDeviceAddedToDs(self):
        '''
        get the value of server_id in ds_device_info to see if the device
        added to DS successfully. 
        '''
        try:
            log.debug("test if device added to a DS")
            #sleep some time to wait the device added to DS
            log.debug("sleep 40 seconds to wait DS register")
            time.sleep(40)
            
            device = Mysql(self.con).getDevice()
            deviceId = device[0][0]#the first filed in devices is deviceId
            dsDeviceInfo = Mysql(self.con).getDsDeviceInfo(deviceId)
            dsId = dsDeviceInfo[0][4]
            log.debug("ds_device_info=%s", dsDeviceInfo)
            if dsId == -1:
                raise Exception("maybe device has not added to DS")
            log.debug("added to DS correctly")
        except Exception,e:
            log.error("exception, %s", e)
            raise Exception("maybe device has not added to DS")
        
    def testMatchUpInChannelDeviceMap(self):
        '''
        See if the matchup in channel_device_map is correct
        '''
        try:
            device = Mysql(self.con).getDevice()
            deviceId = device[0][0]
            
            #on Kai-node, check the channel_device matchup
            log.debug("test channel_device_map")
            map = Mysql(self.con).getChannelDeviceMap()
            log.debug("channel-device-map=%s",map)
            #if there is device_id in the channel_device_map, then the map is correct
            if len(map) != 0:
                for each in map:
                    #node_device_id
                    nodeDeviceId = each[2]
                    if (nodeDeviceId == deviceId):
                        log.debug("device_channel map is correct.") 
            raise Exception("maybe")
        except Exception,e:
            log.error("exception, %s", e)
            raise Exception("device-channel-map exception")
        #on KUP, the judge process will be different 
        
    def testIfDeviceUpdated(self):
        '''
        check if the device's host updated to the new one correctly
        in devices and ds_device_info
        '''
        try:
            log.debug("test if device updated correctly")
            #get device's id whose name is "unittest-amtk" 
            device = Mysql(self.con).getDevice()
            deviceId = device[0][0]#the first filed in devices is deviceId
            updatedHost = device[0][3]
            log.debug("updated host=%s", updatedHost)
            
            #if this device updated correctly in devices
            hostUpdatedInDevices = False
            #get the updated host from configuration.cfg
            intendedHost = Config().getFromConfigs(Constants.updateDevice, "host")
            if intendedHost !=  updatedHost:
                hostUpdatedInDevices = True
            
            #select from ds_device_info to verify if the device's host updated successfully        
            dsDeviceInfo = Mysql(self.con).getDsDeviceInfo(deviceId)
            log.debug("ds_device_info=%s",dsDeviceInfo)
            #the second one is device_info which contains device's host
            deviceInfo = dsDeviceInfo[0][2]
            hostUpdatedInDsDevInfo = False
            if intendedHost in deviceInfo:
                hostUpdatedInDsDevInfo = True
            
            #only if host updated in devices and ds_device_info, the update is successful
            if hostUpdatedInDevices == False | hostUpdatedInDsDevInfo == False:
                raise Exception("device updated fail")
            
            #self.assertEqual(hostUpdated, True,"maybe device update fail")
            log.debug("device updated correctly")
        except Exception,e:
            log.error("exception, %s", e)
            raise Exception("")
        
    def testIfDeviceDeleted(self):
        '''
        check data in devices\ds_device_info, to see if the device is deleted correclty
        '''
        try:
            log.debug("test if device deleted correctly")
            #get device's id whose name is "unittest-amtk" 
            device = Mysql(self.con).getDevice()
            log.debug("deleted device=%s",device)
            
            deviceId = Config().getFromConfigs(Constants.deleteDevice, "device-id")
            dsDeviceInfo = Mysql(self.con).getDsDeviceInfo(deviceId)
            log.debug("deleted dsDeviceInfo=%s",dsDeviceInfo)
            log.debug("len-device=" + (str)(len(device)) + ",len-dsDevice_info=" + (str)(len(dsDeviceInfo)) )
            if (len(device) == 0) & (len(dsDeviceInfo) == 0):
                log.debug("device deleted correctly")
            else:
                raise Exception("maybe device deleted fail")
        except Exception,e:
            log.error("exception, %s", e)
            raise Exception("device deleted exception")
        
    def cleanDeviceInfo(self):
        device = Mysql(self.con).getDevice()
        log.debug("deleted device=%s",device)
        deviceId = Config().getFromConfigs(Constants.deleteDevice, "device-id")
        result = Mysql(self.con).cleanDeviceInfo(deviceId)
        log.debug("clean device, result=%s",result)
    
    def testIfAddedToStreamSessionInfo(self):
        '''
        check if added to stream_session_info correctly
        '''
        deviceId = Config().getFromConfigs(Constants.deleteDevice, "device-id")
        streamSessionInfo = Mysql(self.con).getStreamSessionInfo(deviceId)
        log.debug("streamSessionInfo=%s",streamSessionInfo)
        if streamSessionInfo != None:
            log.debug("add to stream_session_info success.")
        else:
            raise Exception("add to stream_session_info fail.")
    
    def testIfDelFromStreamSessionInfo(self):
        '''
        check if delete from stream_session_info correctly when the session is timeout
        '''
        #sleep sometime between check the streamSessionInfo
        ttl = Config().getFromConfigs(Constants.streamControl, "ttl")
        timeToSleep = int(ttl) + 10
        time.sleep(timeToSleep)
        log.debug("sleep %s seconds before test delete stream_session_info", timeToSleep)
        
        deviceId = Config().getFromConfigs(Constants.deleteDevice, "device-id")
        streamSessionInfo = Mysql(self.con).getStreamSessionInfo(deviceId)
        log.debug("streamSessionInfo=%s",streamSessionInfo)
        if len(streamSessionInfo) == 0:
            log.debug("delete stream_session_info success.")
        else:
            raise Exception("delete from stream_session_info fail.")
        
        
    #----some auxiliary methods
    def isExist(self):
        pass   
        
        
        