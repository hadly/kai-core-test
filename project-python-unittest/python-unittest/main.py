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
from arbiter.TestDeviceControlService import DeviceControlServiceClient
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
        self.dcs = DeviceControlServiceClient()
        log.debug('******** Main init end**********')
    def beginTesting(self):
        '''
        Note:在这个函数里面添加要进行的测试方法;
        '''
        
        fail = 0
        log.info("[TP-Set KUP Address][begin]")
        setKupResult = self.testSetKUP()
        if setKupResult == -1:
            fail += 1
            log.info("[TP-Set KUP Address][end]               False \n")
        else:
            log.info("[TP-Set KUP Address][end]               OK \n")
            
            
            log.info("[TP-Add Device][begin]")
            result = self.dms.testAddDevice()
            if result:
                log.info("call addDevice                          OK")
                addResult = self.testIsAddDeviceSuccess()
                if addResult:
                    log.info("[TP-Add Device][end]                    OK \n")
#                    time.sleep(90)
                   
                    
                    log.info("[TP-Liveview][begin]")
                    liveviewRes = self.testLiveViewAndFrameRate() #-1/1
                    if liveviewRes==-1:
                        fail += 1
                        log.info("[TP-Liveview][end]                      False \n")
                    else:
                        log.info("[TP-Liveview][end]                      OK \n")
                    
                    
                    log.info("[TP-Is Device Online][begin]")
                    getDeviceStatus = self.testGetDeviceStatus()
                    if getDeviceStatus == -1:
                        fail += 1
                        log.info("[TP-Is Device Online][end]                False \n")
                    else:
                        log.info("[TP-Is Device Online][end]                OK \n")
                   
                    
                    log.info("[TP-Stream Session][begin]")
                    sessionResult = self.scs.controlSession()
                    if sessionResult == -1:
                        fail += 1
                        log.info("[TP-Stream Session][end]                False \n")
                    else:
                        log.info("[TP-Stream Session][end]                OK \n")
                    
                    
                    log.info("[TP-Update ChunkSize][begin]")
                    chunksizeResult = self.testChunkSize() #-1/1
                    if chunksizeResult == -1:
                        fail += 1
                        log.info("[TP-Update ChunkSize][end]              False \n")
                    else:
                        log.info("[TP-Update ChunkSize][end]              OK \n")
                    
                    
                    log.info("[TP-Set Storage Space][begin]")
                    if self.testStreamStorageLimitZero() == 1:
                        if self.testStreamStorageLimitOther() == 1:
                            log.info("[TP-Set Storage Space][end]             OK \n")
                        else:
                            log.info("[TP-Set Storage Space][end]             False \n")
                    else:
                        log.info("[TP-Set Storage Space][end]             False \n")
                    
                    
                    log.info("[TP-Video Recording][begin]")
                    videoStorageRes = self.testVideoStore()#-1/1
                    if videoStorageRes == -1:
                        fail += 1
                        log.info("[TP-Video Recording][end]               False \n")
                    else:
                        log.info("[TP-Video Recording][end]               OK \n")
                    
                    
                    log.info("[TP-Image Recording][begin]")
                    imageStorageRes = self.testPhotoStore()#-1/1
                    if imageStorageRes == -1:
                        fail += 1
                        log.info("[TP-Image Recording][end]               False \n")
                    else:
                        log.info("[TP-Image Recording][end]               OK \n")
                    
                    
                    log.info("[TP-Event Video Recording][begin]")
                    eventVideoRes = self.testVideoEvent()#-1/1
                    if eventVideoRes == -1:
                        fail += 1
                        log.info("[TP-Event Video Recording][end]         False \n")
                    else:
                        log.info("[TP-Event Video Recording][end]         OK \n")
                    log.info("we will test updateDevice, please wait")
                    
                    
                    log.info("[TP-Update Device][begin]")
                    updateDeviceRes = self.testUpdateDevice()
                    if updateDeviceRes==-1:
                        fail += 1
                        log.info("[TP-Update Device][end]                 False \n")
                    else:
                        log.info("[TP-Update Device][end]                 OK \n")                  
                    
                    
                    log.info("[TP-Delete Device][begin]")
                    delDeviceRes = self.dms.testDeleteDevice()
                    isSuccess = self.dataVerifier.testIfDeviceDeleted()
                    if delDeviceRes and isSuccess:
                        log.info("[TP-Delete Device][end]                 OK \n")
                    else:
                        fail += 1
                        log.info("[TP-Delete Device][end]                 False \n")
                else:
                    fail += 1
                    log.info("[TP-Add Device][end]               False \n")
        
        if fail==0:
            log.info("Congratulations!!! Your testing is successful.")
        else:
            log.warn("something wrong during this test, please refer to the log above, and search for 'False' to locate the errors.")
        
    def testSetKUP(self):
        result = self.ccs.testSetCloudServer()
        if result:
            log.info("set KUP address                         OK")
        else:
            log.info("set KUP address                         False")
        dbResult = self.dataVerifier.testConfigurationsHavKUP()
        if dbResult:
            log.info("is KUP address in table Configurations  OK")
        else:
            log.info("is KUP address in table Configurations  False")
        if result and dbResult:
            return 1
        else:
            return -1
    
    def testUpdateDevice(self):
        #update Device
        upDeviceRes = self.dms.testUpdateDevice()
        if upDeviceRes:
            log.info("call updateDevice                       OK")
            result = self.testIsAddDeviceSuccess()
            if result:
                log.info("is device correct in DB and DS          OK")
                if self.testLiveViewAndFrameRate()==1:
                    log.info("is liveview correct                     OK")
                    return 1
                else:
                    log.info("is liveview correct                     False")
                    return -1
            else:
                log.info("is device correct in DB and DS          False")
                return -1
        else:
            log.info("call updateDevice                       False")
            return -1
        
    def testIsAddDeviceSuccess(self):
        isInDevices = self.dataVerifier.testCorrectnessInDevices()
        if isInDevices:
            log.info("is device in table Devices              OK")
        else:
            log.info("is device in table Devices              False")
        
        isInDsDevInfo = self.dataVerifier.testCorrectnessInDsDeviceInfo()
        if isInDsDevInfo:
            log.info("is device in table ds_device_info       OK")
        else:
            log.info("is device in table ds_device_info       False")
        
        isAddedToDS = self.dataVerifier.testIfDeviceAddedToDs()
        if isAddedToDS:
            log.info("is device added to a DS                 OK")
        else:
            log.info("is device added to a DS                 False")
        #dataVerifier.testMatchUpInChannelDeviceMap()        
        #is this device in DS by calling getDevices()
        time.sleep(3)
        global ds 
        ds = DeviceServerServiceClient()
        isInDS = ds.testDeviceisinDs()
        if isInDS:
            log.info("does device exists in DS                OK")
        else:
            log.info("does device exists in DS                False")
        
        if isInDevices and isInDsDevInfo and isAddedToDS and isInDS:
            return True
        else:
            return False
    
    def testLiveViewAndFrameRate(self):
        viewRes = self.testLiveView(self.scs, self.dataVerifier)
        if viewRes:
            log.info("liveview URL                            OK")
        else:
            log.info("liveview URL                            False")        
        rateRes = ds.testDeviceFrameRate()#测试帧率
        if rateRes:
            log.info("liveview frame rate                     OK")
        else:
            log.info("liveview frame rate                     False")
        if viewRes and rateRes:
            return 1
        else:
            return -1
        
    def testGetDeviceStatus(self):
        result = self.dcs.judgeDeviceStatus()
        if result == "online":
            log.info("Device Online                OK")
            return 1
        else:
            log.info("Device Online                False")
            return -1
        
    def testStreamStorageLimitZero(self):
        global rss
        rss = RecordingServerServiceClient()
        if self.dms.beginVideoRecording():
            begin_local_time = time.strftime("%d%m%Y%H%M%S",time.localtime(time.time()))
            log.debug('begin_local_time : %s',begin_local_time)
            time.sleep(40)
            result = self.streamStorageLimitStrategy(0, 120, 180, begin_local_time,0)
            if result:
                return 1
            else:
                return -1
        else:
            return -1
    
    def testStreamStorageLimitOther(self):
        if self.dms.beginVideoRecording():
            begin_local_time = time.strftime("%d%m%Y%H%M%S",time.localtime(time.time()))
            log.debug('begin_local_time : %s',begin_local_time)
            time.sleep(40)
            log.debug('message: next will wait time 130s for test 10M')
            one_result = self.streamStorageLimitStrategy(10, 130, 210, begin_local_time,1)
            log.debug('message:next will wait time  150s for test 30M')
            two_result = self.streamStorageLimitStrategy(30, 0, 150, begin_local_time,2)
            if one_result and two_result:
                return 1
            else:
                return -1
        else:
            return -1
    
    def streamStorageLimitStrategy(self,size,onesleeptime,twosleeptime,begin_local_time,number):
        result = self.ccs.testSetStreamLimit(size)
        log.debug('set stream list size, result=', result)
        if result:
            log.info('set storage space is %dM                OK',size)
            time.sleep(onesleeptime)
            end_local_time = time.strftime("%d%m%Y%H%M%S",time.localtime(time.time()))
            log.debug('end_local_time : %s',end_local_time)
            if size == 0:
                if self.dms.stopVideoRecording():
                    log.debug('close video time :')
                    time.sleep(twosleeptime)
                    log.debug('RecordingServerService : %s',rss)
                    if rss is None:
                        raise Exception("RecordingServerService NoneType")
                    zero_first_video_begin = rss.getVideoStreamList_FirstValue(begin_local_time,end_local_time)
                    if zero_first_video_begin is None:
                        log.info('test storage space is 0M                OK')
                        return True
                    else:
                        log.info('test storage space is 0M                False')
                        return False
                else:
                    return False
             
            #get the first video before RS cleaned the videos
            first_video_begin = rss.getVideoStreamList_FirstValue(begin_local_time,end_local_time)
            log.debug('first_video_begin :%s',first_video_begin)
            time.sleep(twosleeptime)
            
            #get the first video after RS cleans the videos
            end_local_time = time.strftime("%d%m%Y%H%M%S",time.localtime(time.time()))
            second_video_begin = rss.getVideoStreamList_FirstValue(begin_local_time,end_local_time)
            log.debug('second_video_begin : %s',second_video_begin)
            
            #compare the first video before and after RS cleaned, verify if the result is correct 
            if number == 1 and first_video_begin != second_video_begin:
                log.info('test storage space is %sM                OK',size)
                return True
            elif number == 1 and first_video_begin == second_video_begin:
                log.info('test storage space is %sM                False',size)
                return False
            
            if number == 2 and first_video_begin == second_video_begin:
                log.info('test storage space is %sM                OK',size)
                self.dms.stopVideoRecording()
                return True
            elif number == 2 and first_video_begin != second_video_begin:
                log.info('test storage space is %sM                False',size)
                return False
        else:
            log.info('set storage space is %dM                 False',size)
            return False

    
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
          test video recording
        '''
        result = self.dms.TestVideoStrategy()
        if result:
            log.info("execute video recording strategy        OK")
            time.sleep(15)
            videoUrlOK = self.scs.checkVideoListSize()
            if videoUrlOK:
                log.info("video recording URL                     OK")
            else:
                log.info("video recording URL                     False")
            
#             global rss
#             rss = RecordingServerServiceClient()
            videoContentOK = rss.testGetVideoStreamList()
            if videoContentOK:
                log.info("video recording frateRate/duration      OK")
            else:
                log.info("video recording frateRate/duration      False")
            
            if videoUrlOK and videoContentOK:
                return 1
            else:
                return -1
        else:
            log.info("execute video recording strategy        False")
            return -1 
        
    def testPhotoStore(self):
        '''
          test photo
        '''
        result = self.dms.testPhotoStrategy()
        if result:
            log.info("execute image recording strategy        OK")
            imageUrlOK = self.scs.checkPhotoUrlSize()
            if imageUrlOK:
                log.info("image recording URL                     OK")
            else:
                log.info("image recording URL                     False")
            
            imageContentOK = rss.testGetPhotoStreamList()
            if imageContentOK:
                log.info("image recording content check           OK")
            else:
                log.info("image recording content check           False")
            if imageUrlOK and imageContentOK:
                return 1
            else:
                return -1
        else:
            log.info("execute image recording strategy         False")
            return -1
    def testVideoEvent(self):
        '''
          test video-event,cycles time is 6
        '''
        isTrue = True
        num = 0
        sum = 1
        upres = self.dms.beginVideoRecording()
        if upres:
            time.sleep(40)
        while isTrue:
            log.info('[%d] the %d round event video recording...', num, num)
            result = self.drs.sendEventToArbiter()
            if result:
                log.info("send event video to Arbiter             OK")
                time.sleep(10)
                eventContentOK = rss.testGetEventStreamList()
                if eventContentOK:
                    log.info("event video content check               OK")
                    sum += 1
                else:
                    log.info("event video content check               False")
            else:
                log.info("send event video to Arbiter             False")
            num = num + 1
            if num == 6:
                isTrue = False
                if sum >= 5:
                    return 1
                else:
                    return -1
    
    def testLiveView(self, scs, dataVerifier):
        # check the if the liveview URL is correct 
        urlResult = scs.testLiveViewResultUrl()
        addResult = dataVerifier.testIfAddedToStreamSessionInfo()
        delResult = dataVerifier.testIfDelFromStreamSessionInfo()
        if urlResult and addResult and delResult:
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
