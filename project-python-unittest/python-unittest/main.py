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
        self.dms = DeviceManagementServer()
        self.dataVerifier = MysqlDataVerifier()
        self.scs = StreamControlServer()
        self.ds = DeviceServerService()
        self.ccs = ConfigControlService()
        self.drs = DeviceDataReceiverService()
        self.res = RecordingServerService()
    
    def beginTesting(self):
        '''
        Note:����������������Ҫ���еĲ��Է���;
        '''
        
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
        self.dms.testAddDevice()
        self.stepOne()
        #2
        self.stepTwo()
        #3
        self.stepThree()
        #4
        self.stepFour()
        #5
        self.stepFive()
        #6
        self.stepSix()       
       
        
        ####7.�����豸
        self.dms.testUpdateDevice()
        self.stepOne()
        self.stepTwo()
        self.stepFour()
        self.stepFive()
        self.stepSix()
        
        ####8.ɾ���豸
        #ɾ���豸-->�鿴devices\ds_device_info�ȱ����Ƿ�ɾ���ɾ�
        self.dms.testDeleteDevice()
        self.dataVerifier.testIfDeviceDeleted()
        
    def stepOne(self):
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
        
        self.dataVerifier.testCorrectnessInDevices()
        self.dataVerifier.testCorrectnessInDsDeviceInfo()
        self.dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #����DS���Ƿ��и��豸�Ĵ���
        self.ds.testDeviceisinDs()
    
    def stepTwo(self):
        ####2.liveview�鿴����
        #�鿴liveview-->�鿴���ص�liveview�Ƿ���ȷ-->�жϷ��ص�liveview�Ƿ�ɲ���-->
        #-->�鿴stream_session_info�����Ƿ����session��Ϣ-->
        self.testLiveView(self.scs, self.dataVerifier)#����url
        self.ds.testDeviceFrameRate()#����֡��
    
    def stepThree(self):
        '''
          test set chunk-size function
        '''
        self.ccs.testSetChunkSize()
    
    
    def stepFour(self):
        '''
          test video 
        '''  
        self.dms.TestVideoStrategy()
        time.sleep(10)
        self.scs.checkVideoListSize()
        self.res.testGetVideoStreamList() 
        
    def stepFive(self):
        '''
          test photo
        '''
        self.dms.testPhotoStrategy()
        self.scs.checkPhotoUrlSize()
        self.res.testGetPhotoStreamList()  
        
    def stepSix(self):
        '''
          test video-event,cycles time is 6
        '''
        isTrue = True
        num = 0
        while isTrue:
            log.debug('The %d cycles start:',num)
            self.drs.sendEventToArbiter()
            time.sleep(3)
            self.res.testGetEventStreamList()
            log.debug('The %d cycles end:',num)
            num = num + 1
            if num == 6:
                isTrue = False
    
    def testLiveView(self, scs, dataVerifier):
        #�����豸-->�鿴devices���и����Ƿ�ɹ�-->�鿴ds_device_info�����Ƿ�ɹ�-->
        #-->����֮����"2"�в���鿴liveview-->
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
        #����ʲôʱ���׳��쳣,��Ҫ����ӵĲ����豸���
        log.debug("clean environment")
        MainClass().deleteDeviceAndCleanData()
        
        
        
        

    
    