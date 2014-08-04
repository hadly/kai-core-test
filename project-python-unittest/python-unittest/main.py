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
        Note:����������������Ҫ���еĲ��Է���;
        '''
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
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
       
        
#         ####7.�����豸
#         self.dms.testUpdateDevice()
#         self.testAddDeviceIsSuccess()
#         self.testLiveViewAndFrameRate()
#         self.testVideoStore()
#         self.testPhotoStore()
#         self.testVideoEvent()
        
#         ####8.ɾ���豸
#         #ɾ���豸-->�鿴devices\ds_device_info�ȱ����Ƿ�ɾ���ɾ�
#         self.dms.testDeleteDevice()
#         self.dataVerifier.testIfDeviceDeleted()
#         
    def testAddDeviceIsSuccess(self):
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
        
        self.dataVerifier.testCorrectnessInDevices()
        self.dataVerifier.testCorrectnessInDsDeviceInfo()
        self.dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #����DS���Ƿ��и��豸�Ĵ���
        global ds
        ds = DeviceServerServiceClient()
        ds.testDeviceisinDs()
    
    def testLiveViewAndFrameRate(self):
        ####2.liveview�鿴����
        #�鿴liveview-->�鿴���ص�liveview�Ƿ���ȷ-->�жϷ��ص�liveview�Ƿ�ɲ���-->
        #-->�鿴stream_session_info�����Ƿ����session��Ϣ-->
        self.testLiveView(self.scs, self.dataVerifier)#����url
        global ds
        ds.testDeviceFrameRate()#����֡��
    
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
        #����ʲôʱ���׳��쳣,��Ҫ����ӵĲ����豸���
        log.debug("clean environment")
        MainClass().deleteDeviceAndCleanData()
