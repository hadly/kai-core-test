# -*- coding: GBK -*-
'''
Created on 2014-6-19

@author: Administrator
'''
from arbiter.TestDeviceManagementServer import DeviceManagementServer
from arbiter.TestMysqlDataVerifier import MysqlDataVerifier
from arbiter.TestStreamControlServer import StreamControlServerClient
from arbiter.TestConfigControlService import ConfigControlServiceClient
from arbiter.TestDeviceDataReceiverService import DeviceDataReceiverServiceClient
from arbiter.TestRecordingServerService import RecordingServerServiceClient
from arbiter.TestDeviceServerService import DeviceServerServiceClient
import logging
import sys
import time
log = logging.getLogger("MainClass")
class MainClass(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        log.debug('******** Main init begin**********')
        self.dms = DeviceManagementServer()
        self.dataVerifier = MysqlDataVerifier()
        self.scs = StreamControlServerClient()
        self.ccs = ConfigControlServiceClient()
        self.drs = DeviceDataReceiverServiceClient()
        self.res = RecordingServerServiceClient()
        log.debug('******** Main init end**********')
    def beginTesting(self):
        '''
        Note:在这个函数里面添加要进行的测试方法;
        '''
        ####1.添加设备过程
        #添加设备-->查看devices表中添加是否正确-->查看ds_device_info表中是否正确-->
        #-->查看ds_device_info表中device是否添加到DS了-->查看channel_device_map表中的对应关系建立的是否正确
        self.dms.testAddDevice()
        self.testAddDeviceIsSuccess()
        #2
        self.testLiveViewAndFrameRate()
        #3
        self.testChunkSize()
        #4
        self.testVideoStore()
        #5
        self.testPhotoStore()
        #6
        self.testVideoEvent()       
       
        
#         ####7.更新设备
#         self.dms.testUpdateDevice()
#         self.testAddDeviceIsSuccess()
#         self.testLiveViewAndFrameRate()
#         self.testVideoStore()
#         self.testPhotoStore()
#         self.testVideoEvent()
        
#         ####8.删除设备
#         #删除设备-->查看devices\ds_device_info等表中是否删除干净
#         self.dms.testDeleteDevice()
#         self.dataVerifier.testIfDeviceDeleted()
#         
    def testAddDeviceIsSuccess(self):
        ####1.添加设备过程
        #添加设备-->查看devices表中添加是否正确-->查看ds_device_info表中是否正确-->
        #-->查看ds_device_info表中device是否添加到DS了-->查看channel_device_map表中的对应关系建立的是否正确
        
        self.dataVerifier.testCorrectnessInDevices()
        self.dataVerifier.testCorrectnessInDsDeviceInfo()
        self.dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #测试DS中是否有该设备的存在
        global ds
        ds = DeviceServerServiceClient()
        ds.testDeviceisinDs()
    
    def testLiveViewAndFrameRate(self):
        ####2.liveview查看过程
        #查看liveview-->查看返回的liveview是否正确-->判断返回的liveview是否可播放-->
        #-->查看stream_session_info里面是否存了session信息-->
        self.testLiveView(self.scs, self.dataVerifier)#测试url
        global ds
        ds.testDeviceFrameRate()#测试帧率
    
    def testChunkSize(self):
        '''
          test set chunk-size function
        '''
        self.ccs.testSetChunkSize()
    
    
    def testVideoStore(self):
        '''
          test video 
        '''  
        self.dms.TestVideoStrategy()
#         log.debug('VideoStrategy End , will waite 20s ')
#         time.sleep(20)
        self.scs.checkVideoListSize()
        global res
        res = RecordingServerServiceClient()
        res.testGetVideoStreamList() 
        
    def testPhotoStore(self):
        '''
          test photo
        '''
        self.dms.testPhotoStrategy()
        self.scs.checkPhotoUrlSize()
        global res
        res.testGetPhotoStreamList()  
        
    def testVideoEvent(self):
        '''
          test video-event,cycles time is 6
        '''
        isTrue = True
        num = 0
        while isTrue:
            log.info('The %d cycles start:',num)
            self.drs.sendEventToArbiter()
            time.sleep(3)
            global res
            res.testGetEventStreamList()
            log.info('The %d cycles end:',num)
            num = num + 1
            if num == 6:
                isTrue = False
    
    def testLiveView(self, scs, dataVerifier):
        #更新设备-->查看devices表中更新是否成功-->查看ds_device_info更新是否成功-->
        #-->更新之后按照"2"中步骤查看liveview-->
        scs.testLiveViewResult()   
        dataVerifier.testIfAddedToStreamSessionInfo()
        dataVerifier.testIfDelFromStreamSessionInfo()
    
    def deleteDeviceAndCleanData(self):
        try:
            DeviceManagementServer().testDeleteDevice()
        except Exception,e:
            log.error("exception,%s", e)
            self.deleteDeviceAndCleanData()
        #clean device data
        dataVerifier = MysqlDataVerifier()
        dataVerifier.cleanDeviceInfo()

if __name__ == '__main__':
    print "begin Main test."
#     print sys.path
    try:
        MainClass().beginTesting()
#         MainClass().deleteDeviceAndCleanData()
        log.debug("Congratulations!!! Your testing is successful.")
    except Exception,e:
        log.error("exception, %s", e)
        #不管什么时候抛出异常,都要将添加的测试设备清除
        log.debug("clean environment")
        MainClass().deleteDeviceAndCleanData()
