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
        result = self.dms.testAddDevice()
        if result:
            addResult = self.testAddDeviceIsSuccess()
            if addResult:
                fail = 0
                log.info("添加设备成功，开始常规功能测试,此过程预期几十分到好几十分，请耐心等待：")
                log.info("开始视频直播测试")
                resNum1 = self.testLiveViewAndFrameRate() #-1/1
                if resNum1==-1:
                    fail += 1
                    log.info("testLiveViewAndFrameRate                                                false")
                log.info("开始更新ChunkSize测试")
                resNum2 = self.testChunkSize() #-1/1
                if resNum2 == -1:
                    fail += 1
                    log.info("testChunkSize                                                           false")
                log.info("开始视频存储测试")
                resNum3 = self.testVideoStore()#-1/1
                if resNum3 == -1:
                    fail += 1
                    log.info("testVideoStore                                                          false")
                log.info("开始照片存储测试")
                resNum4 = self.testPhotoStore()#-1/1
                if resNum4 == -1:
                    fail += 1
                    log.info("testPhotoStore                                                          false")
                log.info("开始存储视频事件测试")
                resNum5 = self.testVideoEvent()#-1/1
                if resNum5 == -1:
                    fail += 1
                    log.info("testVideoEvent                                                          false")
                sum = resNum1+resNum2+resNum3+resNum4+resNum5
                log.info("sum:%d",sum)
                log.info("共测试%d步，成功%d步,失败%d步,具体失败情况请查看以上日志！",sum,sum-fail,fail)
                log.info("常规测试到此结束！感谢您的耐心等待,下面将执行删除，清空测试,以便恢复系统原貌:！")
                self.dms.testDeleteDevice()
                self.dataVerifier.testIfDeviceDeleted()
                log.info("测试结束，感谢支持！！！")
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
        ####1.添加设备过程
        #添加设备-->查看devices表中添加是否正确-->查看ds_device_info表中是否正确-->
        #-->查看ds_device_info表中device是否添加到DS了-->查看channel_device_map表中的对应关系建立的是否正确
        
        r = self.dataVerifier.testCorrectnessInDevices()
        e = self.dataVerifier.testCorrectnessInDsDeviceInfo()
        s = self.dataVerifier.testIfDeviceAddedToDs()
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #测试DS中是否有该设备的存在
        global ds
        ds = DeviceServerServiceClient()
        u = ds.testDeviceisinDs()
        if r and e and s and u:
            return True
        else:
            return False
        
    
    def testLiveViewAndFrameRate(self):
        ####2.liveview查看过程
        #查看liveview-->查看返回的liveview是否正确-->判断返回的liveview是否可播放-->
        #-->查看stream_session_info里面是否存了session信息-->
        viewRes = self.testLiveView(self.scs, self.dataVerifier)#测试url
        global ds
        rateRes = ds.testDeviceFrameRate()#测试帧率
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
        #不管什么时候抛出异常,都要将添加的测试设备清除
        log.debug("clean environment")
        MainClass().deleteDeviceAndCleanData()
