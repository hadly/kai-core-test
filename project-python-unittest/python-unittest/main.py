# -*- coding: GBK -*-
'''
Created on 2014-6-19

@author: Administrator
'''
from arbiter.TestDeviceManagementServer import DeviceManagementServer
from arbiter.TestMysqlDataVerifier import MysqlDataVerifier
from arbiter.TestStreamControlServer import StreamControlServer
from arbiter.TestConfigControlService import ConfigControlService
from arbiter.TestDeviceDataReceiverService import DeviceDataReceiverService
from arbiter.TestRecordingServerService import RecordingServerService
from arbiter.TestDeviceServerService import DeviceServerService
from arbiter.utils import LogUtil
import sys
import time
log = LogUtil.getLog("MainClass")
class MainClass(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.dms = DeviceManagementServer()
        self.dataVerifier = MysqlDataVerifier()
        self.scs = StreamControlServer()
        self.ds = DeviceServerService()
        self.ccs = ConfigControlService()
        self.drs = DeviceDataReceiverService()
        self.res = RecordingServerService()
    
    def beginTesting(self):
        '''
        Note:在这个函数里面添加要进行的测试方法;
        '''
        
        ####1.添加设备过程
        #添加设备-->查看devices表中添加是否正确-->查看ds_device_info表中是否正确-->
        #-->查看ds_device_info表中device是否添加到DS了-->查看channel_device_map表中的对应关系建立的是否正确
        self.dms.testAddDevice()
        self.stepOne()
        self.stepTwo()
        self.stepThree()
        self.stepFour()
        self.stepFive()
        self.stepSix()       
       
        
        ####7.更新设备
        self.dms.testUpdateDevice()
        self.stepOne()
        self.stepTwo()
        self.stepFour()
        self.stepFive()
        self.stepSix()
        
        ####8.删除设备
        #删除设备-->查看devices\ds_device_info等表中是否删除干净
        self.dms.testDeleteDevice()
        self.dataVerifier.testIfDeviceDeleted()
        
    def stepOne(self):
        ####1.添加设备过程
        #添加设备-->查看devices表中添加是否正确-->查看ds_device_info表中是否正确-->
        #-->查看ds_device_info表中device是否添加到DS了-->查看channel_device_map表中的对应关系建立的是否正确
        
        self.dataVerifier.testCorrectnessInDevices()
        self.dataVerifier.testCorrectnessInDsDeviceInfo()
        self.dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #测试DS中是否有该设备的存在
        self.ds.testDeviceisinDs()
    
    def stepTwo(self):
        ####2.liveview查看过程
        #查看liveview-->查看返回的liveview是否正确-->判断返回的liveview是否可播放-->
        #-->查看stream_session_info里面是否存了session信息-->
        self.testLiveView(self.scs, self.dataVerifier)#测试url
        self.ds.testDeviceFrameRate()#测试帧率
    
    def stepThree(self):
        self.ccs.testSetChunkSize()
        
    def stepFour(self):
        self.dms.TestVideoStrategy()
        time.sleep(10)
        self.scs.checkVideoListSize()
        self.res.testGetVideoStreamList()  # this step never end
        
    def stepFive(self):
        self.dms.testPhotoStrategy()
        self.scs.checkPhotoUrlSize()
        self.res.testGetPhotoStreamList()  # this step never end
        
    def stepSix(self):   #这个方法还要做修改~,eventId 在每次循环都要更改，现在还未实现
        isTrue = True
        num = 0
        while isTrue:
            self.drs.sendEventToArbiter()
            time.sleep(5)
            self.res.testGetVideoStreamList()
            num = num + 1
            if num == 6:
                isTrue = False
        pass
    
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
        #clean device data
        dataVerifier = MysqlDataVerifier()
        dataVerifier.cleanDeviceInfo()

if __name__ == '__main__':
    print "begin Main test."
    print sys.path
    try:
        MainClass().beginTesting()
        log.debug("Congratulations!!! Your testing is successful.")
    except Exception,e:
        log.error("exception, %s", e)
        #不管什么时候抛出异常,都要将添加的测试设备清除
        log.debug("clean environment")
        MainClass().deleteDeviceAndCleanData()
        
        
        
        

    
    