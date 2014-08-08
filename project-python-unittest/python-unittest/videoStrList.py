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
        self.res = RecordingServerServiceClient()
        self.sc = StreamControlServerClient()
        self.dm = DeviceManagementServer()
        self.drs = DeviceDataReceiverServiceClient()
        log.debug('******** Main init end**********')
    def TestVideoStr0(self):
        print 'come0'
        self.sc.checkVideoListSize()
        print 'out0'
    def TestVideoStr1(self):
        print 'come1'
        self.res.testGetVideoStreamList()
        print 'out1'
    def TestVideoStr4(self):
        print 'come4'
        self.dm.TestVideoStrategy()
        print 'out4'
    
    def TestVideoStr2(self):
        print 'come2'
        self.dm.testPhotoStrategy()
        print 'out2'
    def TestVideoStr3(self):
        print 'come3'
        self.sc.checkPhotoUrlSize()
        print 'out3'
    def TestVideoStr5(self):
        print 'come5'
        self.res.testGetPhotoStreamList()
        print 'out5'
    def TestEventStr9(self):
        isTrue = True
        num = 0
        while isTrue:
            log.debug('The %d cycles start:',num)
            self.drs.sendEventToArbiter()
            time.sleep(3)
            global res
            res = RecordingServerServiceClient()
            time.sleep(3)
            res.testGetEventStreamList()
            log.debug('The %d cycles end:',num)
            num = num + 1
            if num == 2:
                isTrue = False
if __name__ == '__main__':
    print "begin Main test."
#    
#     MainClass().TestVideoStr4()   #Video测试策略
    MainClass().TestVideoStr0()   #测试url 
#     MainClass().TestVideoStr1()   #测试帧率，视频大小
    log.info("fffff")
#     MainClass().TestVideoStr2()
#     MainClass().TestVideoStr3()
#     MainClass().TestVideoStr5()
    MainClass().TestEventStr9()
    