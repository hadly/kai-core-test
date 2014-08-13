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
        fail = 0
        log.info("[���Ե�-����KUP][��ʼ]")
        kupRes = self.testSetKUP()
        if kupRes==-1:
            fail += 1
            log.info("[���Ե�-����KUP][����]                False")
        else:
            log.info("[���Ե�-����KUP][����]                OK")
            log.info("[���Ե�-����豸][��ʼ]")
            result = self.dms.testAddDevice()
            if result:
                log.info("ִ������豸                                                                  OK")
                addResult = self.testAddDeviceIsSuccess()
                if addResult:
                    log.info("[���Ե�-����豸][����]                OK")
                    time.sleep(90)
                    log.info("[���Ե�-��Ƶֱ��][��ʼ]")
                    resNum1 = self.testLiveViewAndFrameRate() #-1/1
                    if resNum1==-1:
                        fail += 1
                        log.info("[���Ե�-��Ƶֱ��][����]                False")
                    else:
                        log.info("[���Ե�-��Ƶֱ��][����]                OK")
                    log.info("[���Ե�-����ChunkSize][��ʼ]")
                    resNum2 = self.testChunkSize() #-1/1
                    if resNum2 == -1:
                        fail += 1
                        log.info("[���Ե�-����ChunkSize][����]            False")
                    else:
                        log.info("[���Ե�-����ChunkSize][����]            OK")
                    log.info("[���Ե�-��Ƶ�洢][��ʼ]")
                    resNum3 = self.testVideoStore()#-1/1
                    if resNum3 == -1:
                        fail += 1
                        log.info("[���Ե�-��Ƶ�洢][����]                False")
                    else:
                        log.info("[���Ե�-��Ƶ�洢][����]                OK")
                    log.info("[���Ե�-��Ƭ�洢][��ʼ]")
                    resNum4 = self.testPhotoStore()#-1/1
                    if resNum4 == -1:
                        fail += 1
                        log.info("[���Ե�-��Ƭ�洢][����]                False")
                    else:
                        log.info("[���Ե�-��Ƭ�洢][����]                OK")
                    log.info("[���Ե�-��Ƶ�¼�][��ʼ]")
                    resNum5 = self.testVideoEvent()#-1/1
                    if resNum5 == -1:
                        fail += 1
                        log.info("[���Ե�-��Ƶ�¼�][����]                False")
                    else:
                        log.info("[���Ե�-��Ƶ�¼�][����]                OK")
                    log.info("���潫���и����豸���ԣ�please wait")
                    log.info("[���Ե�-�����豸][��ʼ]")
                    resNum6 = self.testUpdateDevice()
                    if resNum6==-1:
                        fail += 1
                        log.info("[���Ե�-�����豸][����]                False")
                    else:
                        log.info("[���Ե�-�����豸][����]                OK")
#                     log.info("������Ե��˽�������л�������ĵȴ�,���潫ִ��ɾ������ղ���,�Ա�ָ�ϵͳԭò:��")
                    log.info("[���Ե�-ɾ���豸][��ʼ]")
                    delDeviceRes = self.dms.testDeleteDevice()
                    isSuccess = self.dataVerifier.testIfDeviceDeleted()
                    if delDeviceRes and isSuccess:
                        log.info("[���Ե�-ɾ���豸][����]                OK")
                    else:
                        fail += 1
                        log.info("[���Ե�-ɾ���豸][����]                False")
                else:
                    fail += 1
                    log.info("[���Ե�-����豸][����]                False")
        if fail==0:
            log.info("Congratulations!!! Your testing is successful.")
        else:
            log.info("���β���������鿴������־������False���Ա�õ�������Ϣ~")
        log.info("���Խ�������л֧�֣�����") 
    def testSetKUP(self):
        result = self.ccs.testSetCloudServer()
        if result:
            log.info("����KUPHost                OK")
        else:
            log.info("����KUPHost                False")
        dbResult = self.dataVerifier.testConfigurationsHavKUP()
        if dbResult:
            log.info("KUP�Ƿ���Configurations        OK")
        else:
            log.info("KUP�Ƿ���Configurations        False")
        if result and dbResult:
            return 1
        else:
            return -1
    
    def testUpdateDevice(self):
        #update Device
        upDeviceRes = self.dms.testUpdateDevice()
        if upDeviceRes:
            log.info("[�����豸��Ϣ]                OK")
            result = self.testAddDeviceIsSuccess()
            if result:
                log.info("�豸ע�ᵽ                                            OK")
                if self.testLiveViewAndFrameRate()==1:
                    log.info("��Ƶֱ������                                    OK")
                    return 1
                else:
                    log.info("��Ƶֱ������                                     False")
                    return -1
            else:
                log.info("�豸ע��                                                 False")
                return -1
        else:
            log.info("[�����豸��Ϣ]                False")
            return -1
        
    def testAddDeviceIsSuccess(self):
        ####1.����豸����
        #����豸-->�鿴devices��������Ƿ���ȷ-->�鿴ds_device_info�����Ƿ���ȷ-->
        #-->�鿴ds_device_info����device�Ƿ���ӵ�DS��-->�鿴channel_device_map���еĶ�Ӧ��ϵ�������Ƿ���ȷ
        
        r = self.dataVerifier.testCorrectnessInDevices()
        if r:
            log.info("�豸��Devices                OK")
        else:
            log.info("�豸��Devices                False")
        e = self.dataVerifier.testCorrectnessInDsDeviceInfo()
        if e:
            log.info("�豸��ds_device_info            OK")
        else:
            log.info("�豸��ds_device_info            False")
        s = self.dataVerifier.testIfDeviceAddedToDs()
        if s:
            log.info("ע���豸��DS                OK")
        else:
            log.info("ע���豸��DS                False")
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #����DS���Ƿ��и��豸�Ĵ���
        time.sleep(3)
        global ds
        ds = DeviceServerServiceClient()
        u = ds.testDeviceisinDs()
        if u:
            log.info("DS�д��ڸ��豸                                 OK")
        else:
            log.info("DS�д��ڸ��豸                                 False")
        
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
            log.info("ֱ������URL                OK")
        else:
            log.info("ֱ������URL                False")
        global ds
        rateRes = ds.testDeviceFrameRate()#����֡��
        if rateRes:
            log.info("ֱ������֡��                                                  OK")
        else:
            log.info("ֱ������֡��                                                  False")
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
            log.info("��Ƶ�洢����                                          OK")
            time.sleep(15)
            end = self.scs.checkVideoListSize()
            if end:
                log.info("��Ƶ�洢����URL            OK")
            else:
                log.info("��Ƶ�洢����URL            False")
            global res
            res = RecordingServerServiceClient()
            ending = res.testGetVideoStreamList()
            if ending:
                log.info("��Ƶ�洢��ȡ֡�ʣ�ʱ��                            OK")
            else:
                log.info("��Ƶ�洢��ȡ֡�ʣ�ʱ��                            False")
            if ending and end:
                return 1
            else:
                return -1
        else:
            log.info("��Ƶ�洢����                                                            False")
            return -1 
        
    def testPhotoStore(self):
        '''
          test photo
        '''
        result = self.dms.testPhotoStrategy()
        if result:
            log.info("��Ƭ�洢����                                                           OK")
            end = self.scs.checkPhotoUrlSize()
            if end:
                log.info("��Ƭ�洢���URL                OK")
            else:
                log.info("��Ƭ�洢���URL                False")
            global res
            ending = res.testGetPhotoStreamList()
            if ending:
                log.info("��Ƭ�洢������Ϣ�˲�                                         OK")
            else:
                log.info("��Ƭ�洢������Ϣ�˲�                                          False")
            if end and ending:
                return 1
            else:
                return -1
        else:
            log.info("��Ƭ�洢����                                                   False")
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
                log.info("�����¼���Arbiter                OK")
                time.sleep(10)
                global res
                end = res.testGetEventStreamList()
                if end:
                    log.info("�¼���Ϣ���                                                         OK")
                    sum += 1
                else:
                    log.info("�¼���Ϣ���                                                         False")
            else:
                log.info("�����¼���Arbiter                False")
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
