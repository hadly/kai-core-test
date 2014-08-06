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
        result = self.dms.testAddDevice()
        if result:
            addResult = self.testAddDeviceIsSuccess()
            if addResult:
                fail = 0
                log.info("����豸�ɹ�����ʼ���湦�ܲ���,�˹���Ԥ�ڼ�ʮ�ֵ��ü�ʮ�֣������ĵȴ���")
                log.info("��ʼ��Ƶֱ������")
                resNum1 = self.testLiveViewAndFrameRate() #-1/1
                if resNum1==-1:
                    fail += 1
                    log.info("testLiveViewAndFrameRate                                                false")
                log.info("��ʼ����ChunkSize����")
                resNum2 = self.testChunkSize() #-1/1
                if resNum2 == -1:
                    fail += 1
                    log.info("testChunkSize                                                           false")
                log.info("��ʼ��Ƶ�洢����")
                resNum3 = self.testVideoStore()#-1/1
                if resNum3 == -1:
                    fail += 1
                    log.info("testVideoStore                                                          false")
                log.info("��ʼ��Ƭ�洢����")
                resNum4 = self.testPhotoStore()#-1/1
                if resNum4 == -1:
                    fail += 1
                    log.info("testPhotoStore                                                          false")
                log.info("��ʼ�洢��Ƶ�¼�����")
                resNum5 = self.testVideoEvent()#-1/1
                if resNum5 == -1:
                    fail += 1
                    log.info("testVideoEvent                                                          false")
                sum = resNum1+resNum2+resNum3+resNum4+resNum5
                log.info("sum:%d",sum)
                log.info("������%d�����ɹ�%d��,ʧ��%d��,����ʧ�������鿴������־��",sum,sum-fail,fail)
                log.info("������Ե��˽�������л�������ĵȴ�,���潫ִ��ɾ������ղ���,�Ա�ָ�ϵͳԭò:��")
                self.dms.testDeleteDevice()
                self.dataVerifier.testIfDeviceDeleted()
                log.info("���Խ�������л֧�֣�����")
#         
    def testUpdateDevice(self):
        #update Device
        self.dms.testUpdateDevice()
        self.testAddDeviceIsSuccess()
        self.testLiveViewAndFrameRate()
        self.testVideoStore()
        self.testPhotoStore()
        self.testVideoEvent()
        
    
    def testAddDeviceIsSuccess(self):
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
        
        r = self.dataVerifier.testCorrectnessInDevices()
        e = self.dataVerifier.testCorrectnessInDsDeviceInfo()
        s = self.dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #����DS���Ƿ��и��豸�Ĵ���
        global ds
        ds = DeviceServerServiceClient()
        u = ds.testDeviceisinDs()
        if r and e and s and u:
            return True
        else:
            return False
        
    
    def testLiveViewAndFrameRate(self):
        ####2.liveview�鿴����
        #�鿴liveview-->�鿴���ص�liveview�Ƿ���ȷ-->�жϷ��ص�liveview�Ƿ�ɲ���-->
        #-->�鿴stream_session_info�����Ƿ����session��Ϣ-->
        viewRes = self.testLiveView(self.scs, self.dataVerifier)#����url
        global ds
        rateRes = ds.testDeviceFrameRate()#����֡��
        if viewRes and rateRes:
            return 1
        else:
            return -1
    
    def testChunkSize(self):
        '''
          test set chunk-size function
        '''
        result = self.ccs.testSetChunkSize()
        if result:
            return 1
        else:
            return -1
    
    
    def testVideoStore(self):
        '''
          test video 
        '''
        result = self.dms.TestVideoStrategy()
        if result:
            end = self.scs.checkVideoListSize()
            global res
            res = RecordingServerServiceClient()
            ending = res.testGetVideoStreamList()
            if ending and end:
                return 1
            else:
                return -1 
        
    def testPhotoStore(self):
        '''
          test photo
        '''
        result = self.dms.testPhotoStrategy()
        if result:
            end = self.scs.checkPhotoUrlSize()
            global res
            ending = res.testGetPhotoStreamList()
            if end and ending:
                return 1
            else:
                return -1
        
    def testVideoEvent(self):
        '''
          test video-event,cycles time is 6
        '''
        isTrue = True
        num = 0
        sum = 0
        while isTrue:
            log.info('The %d cycles start:',num)
            result = self.drs.sendEventToArbiter()
            if result:
                time.sleep(3)
                global res
                end = res.testGetEventStreamList()
                if end:
                    sum += 1
                log.info('The %d cycles end:',num)
            num = num + 1
            if num == 6:
                isTrue = False
                if sum >= 4:
                    return 1
                else:
                    return -1
    
    def testLiveView(self, scs, dataVerifier):
        urlResult = scs.testLiveViewResultUrl()
        addRes = dataVerifier.testIfAddedToStreamSessionInfo()
        delRes = dataVerifier.testIfDelFromStreamSessionInfo()
        if urlResult and addRes and delRes:
            return True
        else:
            return False
    
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
