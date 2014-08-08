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
        log.info("[����KUP]")
        kupRes = self.testSetKUP()
        if kupRes==-1:
            log.info("����KUP                                                False")
        else:
            log.info("����KUP                                                OK")
            log.info("[����豸]")
            log.info("��ʼ����豸...")
            result = self.dms.testAddDevice()
            if result:
                log.info("����豸                                                                                                                                                      OK")
                addResult = self.testAddDeviceIsSuccess()
                if addResult:
                    fail = 0
                    log.info("�豸��ӳɹ�����ʼ���湦�ܲ���,�˹���Ԥ�ڼ�ʮ�ֵ��ü�ʮ�֣������ĵȴ���")
                    log.info("[��Ƶֱ��]")
                    log.info("��ʼ��Ƶֱ������...")
                    resNum1 = self.testLiveViewAndFrameRate() #-1/1
                    if resNum1==-1:
                        fail += 1
                        log.info("��Ƶֱ��                                                                                                                                                                                        False")
                    else:
                        log.info("��Ƶֱ��                                                                                                                                                                                        OK")
                    log.info("[����ChunkSize]")
                    log.info("��ʼ����ChunkSize����...")
                    resNum2 = self.testChunkSize() #-1/1
                    if resNum2 == -1:
                        fail += 1
                        log.info("����ChunkSize                                                           False")
                    else:
                        log.info("����ChunkSize                                                           OK")
                    log.info("[��Ƶ�洢]")
                    log.info("��ʼ��Ƶ�洢����...")
                    resNum3 = self.testVideoStore()#-1/1
                    if resNum3 == -1:
                        fail += 1
                        log.info("��Ƶ�洢                                                                                                                                                                                                      False")
                    else:
                        log.info("��Ƶ�洢                                                                                                                                                                                                      OK")
                    log.info("[��Ƶ�¼�]")
                    log.info("��ʼ��Ƶ�¼�����...")
                    resNum5 = self.testVideoEvent()#-1/1
                    if resNum5 == -1:
                        fail += 1
                        log.info("��Ƶ�¼����                                                                                                                                                                                                 False")
                    else:
                        log.info("��Ƶ�¼����                                                                                                                                                                                                 OK")
                    log.info("[��Ƭ�洢]")
                    log.info("��ʼ��Ƭ�洢����...")
                    resNum4 = self.testPhotoStore()#-1/1
                    if resNum4 == -1:
                        fail += 1
                        log.info("��Ƭ�洢                                                                                                                                                                                                        False")
                    else:
                        log.info("��Ƭ�洢                                                                                                                                                                                                        OK")
                    
                    log.info("������%d�����ɹ�%d��,ʧ��%d��,����ʧ�������鿴������־��",5,5-fail,fail)
                    log.info("���潫���и����豸���ԣ�please wait")
                    log.info("[�����豸]")
                    self.testUpdateDevice()
                    log.info("������Ե��˽�������л�������ĵȴ�,���潫ִ��ɾ������ղ���,�Ա�ָ�ϵͳԭò:��")
                    delDeviceRes = self.dms.testDeleteDevice()
                    isSuccess = self.dataVerifier.testIfDeviceDeleted()
                    if delDeviceRes and isSuccess:
                        log.info("ɾ�����ݳɹ������Լ���������")
                    log.info("���Խ�������л֧�֣�����")
         
    def testSetKUP(self):
        result = self.ccs.testSetCloudServer()
        if result:
            log.info("����KUPHost                                        OK")
        else:
            log.info("����KUPHost                                        False")
        dbResult = self.dataVerifier.testConfigurationsHavKUP()
        if dbResult:
            log.info("KUP�Ƿ���Configurations                             OK")
        else:
            log.info("KUP�Ƿ���Configurations                             False")
        if result and dbResult:
            return 1
        else:
            return -1
    
    def testUpdateDevice(self):
        #update Device
        upDeviceRes = self.dms.testUpdateDevice()
        if upDeviceRes:
            log.info("�����豸��Ϣ�ɹ����ּ����º��豸����,������̿�����Ҫ10~20����:")
            result = self.testAddDeviceIsSuccess()
            if result:
                log.info("�豸ע�ᵽDS                                       OK~")
                if self.testLiveViewAndFrameRate()==1:
                    log.info("��Ƶֱ������                                                                                                                  OK~")
                else:
                    log.info("��Ƶֱ������                                                                                                                  False~")
                if self.testVideoStore()==1:
                    log.info("��Ƶ�洢����                                                                                                                 OK~")
                else:
                    log.info("��Ƶ�洢����                                                                                                                 False~")
                if self.testPhotoStore()==1:
                    log.info("ͼƬ�洢����                                                                                                                 OK~")
                else:
                    log.info("ͼƬ�洢����                                                                                                                 False~")
                if self.testVideoEvent()==1:
                    log.info("��Ƶ�¼��洢                                                                                                                 OK~")
                else:
                    log.info("��Ƶ�¼��洢                                                                                                                 False~")
            else:
                log.info("�豸ע��                                                                                                                            False")
        else:
            log.info("�豸����                                                                                                                    false~")
        
    def testAddDeviceIsSuccess(self):
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
        
        r = self.dataVerifier.testCorrectnessInDevices()
        if r:
            log.info("�豸��Devices                                            OK")
        else:
            log.info("�豸��Devices                                            False")
        e = self.dataVerifier.testCorrectnessInDsDeviceInfo()
        if e:
            log.info("�豸��ds_device_info                                     OK")
        else:
            log.info("�豸��ds_device_info                                     False")
        s = self.dataVerifier.testIfDeviceAddedToDs()
        if s:
            log.info("ע���豸��DS                                              OK")
        else:
            log.info("ע���豸��DS                                              False")
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #����DS���Ƿ��и��豸�Ĵ���
        global ds
        ds = DeviceServerServiceClient()
        u = ds.testDeviceisinDs()
        if u:
            log.info("DS�д��ڸ��豸                                                                                                                                      OK")
        else:
            log.info("DS�д��ڸ��豸                                                                                                                                      False")
        
        if r and e and s and u:
            return True
        else:
            return False
        
    
    def testLiveViewAndFrameRate(self):
        ####2.liveview�鿴����
        #�鿴liveview-->�鿴���ص�liveview�Ƿ���ȷ-->�жϷ��ص�liveview�Ƿ�ɲ���-->
        #-->�鿴stream_session_info�����Ƿ����session��Ϣ-->
        viewRes = self.testLiveView(self.scs, self.dataVerifier)#����url
        if viewRes:
            log.info("ֱ������URL                                               OK")
        else:
            log.info("ֱ������URL                                               False")
        global ds
        rateRes = ds.testDeviceFrameRate()#����֡��
        if rateRes:
            log.info("ֱ������֡��                                                                                                                                              OK")
        else:
            log.info("ֱ������֡��                                                                                                                                              False")
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
            log.info("��Ƶ�洢����                                                                                                                                                    OK")
            time.sleep(15)
            end = self.scs.checkVideoListSize()
            if end:
                log.info("��Ƶ�洢����URL                                            OK")
            else:
                log.info("��Ƶ�洢����URL                                            False")
            global res
            res = RecordingServerServiceClient()
            ending = res.testGetVideoStreamList()
            if ending:
                log.info("��Ƶ�洢��ȡ֡�ʣ�ʱ��                                                                                                                           OK")
            else:
                log.info("��Ƶ�洢��ȡ֡�ʣ�ʱ��                                                                                                                           False")
            if ending and end:
                return 1
            else:
                return -1
        else:
            log.info("��Ƶ�洢����                                                                                                                                                            False")
            return -1 
        
    def testPhotoStore(self):
        '''
          test photo
        '''
        result = self.dms.testPhotoStrategy()
        if result:
            log.info("��Ƭ�洢����                                                                                                                                                            OK")
            end = self.scs.checkPhotoUrlSize()
            if end:
                log.info("��Ƭ�洢���URL                                                 OK")
            else:
                log.info("��Ƭ�洢���URL                                                 False")
            global res
            ending = res.testGetPhotoStreamList()
            if ending:
                log.info("��Ƭ�洢������Ϣ�˲�                                                                                                                                            OK")
            else:
                log.info("��Ƭ�洢������Ϣ�˲�                                                                                                                                            False")
            if end and ending:
                return 1
            else:
                return -1
        else:
            log.info("��Ƭ�洢����                                                                                                                                                                False")
            return -1
    def testVideoEvent(self):
        '''
          test video-event,cycles time is 6
        '''
        isTrue = True
        num = 0
        sum = 1
        while isTrue:
            log.info('��%d�β�����Ƶ�¼�...',num)
            self.dms.updateCloud()
            result = self.drs.sendEventToArbiter()
            if result:
                log.info("�����¼���Arbiter                                              OK")
                time.sleep(10)
                global res
                end = res.testGetEventStreamList()
                if end:
                    log.info("�¼���Ϣ���                                                                                                                                                OK")
                    sum += 1
                else:
                    log.info("�¼���Ϣ���                                                                                                                                                False")
            else:
                log.info("�����¼���Arbiter                                              False")
            num = num + 1
            if num == 6:
                isTrue = False
                if sum >= 5:
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
#     print "begin Main test."
#     print sys.path
    try:
        MainClass().beginTesting()
#         MainClass().deleteDeviceAndCleanData()
#         log.debug("Congratulations!!! Your testing is successful.")
    except Exception,e:
        log.error("exception, %s", e)
        #����ʲôʱ���׳��쳣,��Ҫ����ӵĲ����豸���
#         log.debug("clean environment")
        MainClass().deleteDeviceAndCleanData()
