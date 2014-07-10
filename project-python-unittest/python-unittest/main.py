# -*- coding: GBK -*-
'''
Created on 2014-6-19

@author: Administrator
'''
from arbiter.TestDeviceManagementServer import DeviceManagementServer
from arbiter.TestMysqlDataVerifier import MysqlDataVerifier
from arbiter.TestStreamControlServer import StreamControlServer
from arbiter.utils import LogUtil
import sys

log = LogUtil.getLog("MainClass")
class MainClass(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def beginTesting(self):
        '''
        Note:在这个函数里面添加要进行的测试方法;
        '''
        
        #测试类
        dms = DeviceManagementServer()
        dataVerifier = MysqlDataVerifier()
        scs = StreamControlServer()
        
        ####1.添加设备过程
        #添加设备-->查看devices表中添加是否正确-->查看ds_device_info表中是否正确-->
        #-->查看ds_device_info表中device是否添加到DS了-->查看channel_device_map表中的对应关系建立的是否正确
        dms.testAddDevice()
        dataVerifier.testCorrectnessInDevices()
        dataVerifier.testCorrectnessInDsDeviceInfo()
        dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        
        ####2.liveview查看过程
        #查看liveview-->查看返回的liveview是否正确-->判断返回的liveview是否可播放-->
        #-->查看stream_session_info里面是否存了session信息-->
        self.testLiveView(scs, dataVerifier)
        
        ####3.更新设备
        dms.testUpdateDevice()
        dataVerifier.testCorrectnessInDevices()
        dataVerifier.testCorrectnessInDsDeviceInfo()
        dataVerifier.testIfDeviceAddedToDs()
        self.testLiveView(scs, dataVerifier)
        
        ####4.删除设备
        #删除设备-->查看devices\ds_device_info等表中是否删除干净
        dms.testDeleteDevice()
        dataVerifier.testIfDeviceDeleted()
    
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
        
        
        
        

    
    