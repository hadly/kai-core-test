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
        log.info("[设置KUP]")
        kupRes = self.testSetKUP()
        if kupRes==-1:
            log.info("设置KUP                                                False")
        else:
            log.info("设置KUP                                                OK")
            log.info("[添加设备]")
            log.info("开始添加设备...")
            result = self.dms.testAddDevice()
            if result:
                log.info("添加设备                                                                                                                                                      OK")
                addResult = self.testAddDeviceIsSuccess()
                if addResult:
                    fail = 0
                    log.info("设备添加成功，开始常规功能测试,此过程预期几十分到好几十分，请耐心等待：")
                    log.info("[视频直播]")
                    log.info("开始视频直播测试...")
                    resNum1 = self.testLiveViewAndFrameRate() #-1/1
                    if resNum1==-1:
                        fail += 1
                        log.info("视频直播                                                                                                                                                                                        False")
                    else:
                        log.info("视频直播                                                                                                                                                                                        OK")
                    log.info("[更新ChunkSize]")
                    log.info("开始更新ChunkSize测试...")
                    resNum2 = self.testChunkSize() #-1/1
                    if resNum2 == -1:
                        fail += 1
                        log.info("更新ChunkSize                                                           False")
                    else:
                        log.info("更新ChunkSize                                                           OK")
                    log.info("[视频存储]")
                    log.info("开始视频存储测试...")
                    resNum3 = self.testVideoStore()#-1/1
                    if resNum3 == -1:
                        fail += 1
                        log.info("视频存储                                                                                                                                                                                                      False")
                    else:
                        log.info("视频存储                                                                                                                                                                                                      OK")
                    log.info("[视频事件]")
                    log.info("开始视频事件测试...")
                    resNum5 = self.testVideoEvent()#-1/1
                    if resNum5 == -1:
                        fail += 1
                        log.info("视频事件检测                                                                                                                                                                                                 False")
                    else:
                        log.info("视频事件检测                                                                                                                                                                                                 OK")
                    log.info("[照片存储]")
                    log.info("开始照片存储测试...")
                    resNum4 = self.testPhotoStore()#-1/1
                    if resNum4 == -1:
                        fail += 1
                        log.info("照片存储                                                                                                                                                                                                        False")
                    else:
                        log.info("照片存储                                                                                                                                                                                                        OK")
                    
                    log.info("共测试%d步，成功%d步,失败%d步,具体失败情况请查看以上日志！",5,5-fail,fail)
                    log.info("下面将进行更新设备测试，please wait")
                    log.info("[更新设备]")
                    self.testUpdateDevice()
                    log.info("常规测试到此结束！感谢您的耐心等待,下面将执行删除，清空测试,以便恢复系统原貌:！")
                    delDeviceRes = self.dms.testDeleteDevice()
                    isSuccess = self.dataVerifier.testIfDeviceDeleted()
                    if delDeviceRes and isSuccess:
                        log.info("删除数据成功，测试即将结束！")
                    log.info("测试结束，感谢支持！！！")
         
    def testSetKUP(self):
        result = self.ccs.testSetCloudServer()
        if result:
            log.info("设置KUPHost                                        OK")
        else:
            log.info("设置KUPHost                                        False")
        dbResult = self.dataVerifier.testConfigurationsHavKUP()
        if dbResult:
            log.info("KUP是否在Configurations                             OK")
        else:
            log.info("KUP是否在Configurations                             False")
        if result and dbResult:
            return 1
        else:
            return -1
    
    def testUpdateDevice(self):
        #update Device
        upDeviceRes = self.dms.testUpdateDevice()
        if upDeviceRes:
            log.info("更新设备信息成功，现检测更新后设备功能,这个过程可能需要10~20分钟:")
            result = self.testAddDeviceIsSuccess()
            if result:
                log.info("设备注册到DS                                       OK~")
                if self.testLiveViewAndFrameRate()==1:
                    log.info("视频直播测试                                                                                                                  OK~")
                else:
                    log.info("视频直播测试                                                                                                                  False~")
                if self.testVideoStore()==1:
                    log.info("视频存储测试                                                                                                                 OK~")
                else:
                    log.info("视频存储测试                                                                                                                 False~")
                if self.testPhotoStore()==1:
                    log.info("图片存储测试                                                                                                                 OK~")
                else:
                    log.info("图片存储测试                                                                                                                 False~")
                if self.testVideoEvent()==1:
                    log.info("视频事件存储                                                                                                                 OK~")
                else:
                    log.info("视频事件存储                                                                                                                 False~")
            else:
                log.info("设备注册                                                                                                                            False")
        else:
            log.info("设备更新                                                                                                                    false~")
        
    def testAddDeviceIsSuccess(self):
        ####1.添加设备过程
        #添加设备-->查看devices表中添加是否正确-->查看ds_device_info表中是否正确-->
        #-->查看ds_device_info表中device是否添加到DS了-->查看channel_device_map表中的对应关系建立的是否正确
        
        r = self.dataVerifier.testCorrectnessInDevices()
        if r:
            log.info("设备在Devices                                            OK")
        else:
            log.info("设备在Devices                                            False")
        e = self.dataVerifier.testCorrectnessInDsDeviceInfo()
        if e:
            log.info("设备在ds_device_info                                     OK")
        else:
            log.info("设备在ds_device_info                                     False")
        s = self.dataVerifier.testIfDeviceAddedToDs()
        if s:
            log.info("注册设备到DS                                              OK")
        else:
            log.info("注册设备到DS                                              False")
        #dataVerifier.testMatchUpInChannelDeviceMap()
        #测试DS中是否有该设备的存在
        global ds
        ds = DeviceServerServiceClient()
        u = ds.testDeviceisinDs()
        if u:
            log.info("DS中存在该设备                                                                                                                                      OK")
        else:
            log.info("DS中存在该设备                                                                                                                                      False")
        
        if r and e and s and u:
            return True
        else:
            return False
        
    
    def testLiveViewAndFrameRate(self):
        ####2.liveview查看过程
        #查看liveview-->查看返回的liveview是否正确-->判断返回的liveview是否可播放-->
        #-->查看stream_session_info里面是否存了session信息-->
        viewRes = self.testLiveView(self.scs, self.dataVerifier)#测试url
        if viewRes:
            log.info("直播所得URL                                               OK")
        else:
            log.info("直播所得URL                                               False")
        global ds
        rateRes = ds.testDeviceFrameRate()#测试帧率
        if rateRes:
            log.info("直播所得帧率                                                                                                                                              OK")
        else:
            log.info("直播所得帧率                                                                                                                                              False")
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
            log.info("视频存储策略                                                                                                                                                    OK")
            time.sleep(15)
            end = self.scs.checkVideoListSize()
            if end:
                log.info("视频存储所得URL                                            OK")
            else:
                log.info("视频存储所得URL                                            False")
            global res
            res = RecordingServerServiceClient()
            ending = res.testGetVideoStreamList()
            if ending:
                log.info("视频存储获取帧率，时长                                                                                                                           OK")
            else:
                log.info("视频存储获取帧率，时长                                                                                                                           False")
            if ending and end:
                return 1
            else:
                return -1
        else:
            log.info("视频存储策略                                                                                                                                                            False")
            return -1 
        
    def testPhotoStore(self):
        '''
          test photo
        '''
        result = self.dms.testPhotoStrategy()
        if result:
            log.info("照片存储策略                                                                                                                                                            OK")
            end = self.scs.checkPhotoUrlSize()
            if end:
                log.info("照片存储获得URL                                                 OK")
            else:
                log.info("照片存储获得URL                                                 False")
            global res
            ending = res.testGetPhotoStreamList()
            if ending:
                log.info("照片存储所得信息核查                                                                                                                                            OK")
            else:
                log.info("照片存储所得信息核查                                                                                                                                            False")
            if end and ending:
                return 1
            else:
                return -1
        else:
            log.info("照片存储策略                                                                                                                                                                False")
            return -1
    def testVideoEvent(self):
        '''
          test video-event,cycles time is 6
        '''
        isTrue = True
        num = 0
        sum = 1
        while isTrue:
            log.info('第%d次测试视频事件...',num)
            self.dms.updateCloud()
            result = self.drs.sendEventToArbiter()
            if result:
                log.info("发送事件到Arbiter                                              OK")
                time.sleep(10)
                global res
                end = res.testGetEventStreamList()
                if end:
                    log.info("事件信息检测                                                                                                                                                OK")
                    sum += 1
                else:
                    log.info("事件信息检测                                                                                                                                                False")
            else:
                log.info("发送事件到Arbiter                                              False")
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
        #不管什么时候抛出异常,都要将添加的测试设备清除
#         log.debug("clean environment")
        MainClass().deleteDeviceAndCleanData()
