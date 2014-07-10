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
        Note:����������������Ҫ���еĲ��Է���;
        '''
        
        #������
        dms = DeviceManagementServer()
        dataVerifier = MysqlDataVerifier()
        scs = StreamControlServer()
        
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
        dms.testAddDevice()
        dataVerifier.testCorrectnessInDevices()
        dataVerifier.testCorrectnessInDsDeviceInfo()
        dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        
        ####2.liveview�鿴����
        #�鿴liveview-->�鿴���ص�liveview�Ƿ���ȷ-->�жϷ��ص�liveview�Ƿ�ɲ���-->
        #-->�鿴stream_session_info�����Ƿ����session��Ϣ-->
        self.testLiveView(scs, dataVerifier)
        
        ####3.�����豸
        dms.testUpdateDevice()
        dataVerifier.testCorrectnessInDevices()
        dataVerifier.testCorrectnessInDsDeviceInfo()
        dataVerifier.testIfDeviceAddedToDs()
        self.testLiveView(scs, dataVerifier)
        
        ####4.ɾ���豸
        #ɾ���豸-->�鿴devices\ds_device_info�ȱ����Ƿ�ɾ���ɾ�
        dms.testDeleteDevice()
        dataVerifier.testIfDeviceDeleted()
    
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
        
        
        
        

    
    