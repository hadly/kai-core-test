# -*- coding: GBK -*-
'''
Created on 2014-6-18

@author: lizhinian
'''
from CoreServices import StreamControlService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants
from arbiter.utils.Constants import arbiter
import logging
from arbiter.TestStreamControlServer import log

log = logging.getLogger("TestStreamControlServer")
class StreamControlServer():
    client = None 
    
    def __init__(self):
        try:
            host = Config().getFromConfig(arbiter, "arbiter-server-host")
            port = Config().getFromConfig(arbiter, "stream-control-server-port")
            self.client = ThriftClient.getThriftClient(host, port, StreamControlService)
        except Exception, e:
            log.error("StreamControlServer setup:%s",e)
            raise Exception("StreamControlServer setup error")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
    
    def testLiveViewResult(self):
        try:
            log.debug("test begin liveview")
            beginTime = Config().getFromConfig(Constants.streamControl, "liveview-begin-time")
            endTime = Config().getFromConfig(Constants.streamControl, "liveview-end-time")
            type = Config().getFromConfig(Constants.streamControl, "type")
            urls = self.getUrlList(beginTime=beginTime,endTime=endTime,type=type)
            if urls!=None:
                url = urls[0]
            #the returned url is like--rtmp://10.101.0.206:1935/flvplayback/live13-0
                log.debug("liveview,deviceId=%s, urls=%s, url=%s",deviceId,urls,url)
            
                if deviceId not in url:
                    raise Exception("liveview url not normal")
                log.debug("liveview can be played successfully")
        except Exception, e:
            log.error("liveview exception=%s",e)
            raise Exception("liveview exception")
    
    def testBeginPlayBack(self):
        pass
         
    def getUrlList(self,beginTime,endTime,type):
        try:
            sessionId = Config().getFromConfig(Constants.streamControl, "session-id")
            ttl = (long)(Config().getFromConfig(Constants.streamControl, "ttl"))
            channelId = Config().getFromConfig(Constants.streamControl, "channel-id")
            deviceId = Config().getFromConfig(Constants.deleteDevice, "device-id")
            urls = self.client.beginStreamSession(sessionId, ttl, type, None, deviceId, channelId, beginTime, endTime)
            return urls
        except Exception,e:
            raise Exception("geturlList exception")
            return None
    #here are some auxiliary methods
    def checkVideoListSize(self):
        try:
            beginTime = Config().getFromConfig(Constants.streamControl, "liveview-begin-time")
            endTime = Config().getFromConfig(Constants.streamControl, "liveview-end-time")
            type = Config().getFromConfig(Constants.streamControl, "type")
            urls = self.getUrlList(beginTime=beginTime,endTime=endTime,type=type)
            if urls!=None:
                if len(urls)==4:
                    log.debug('the result is success')
                else:
                    log.debug('the result is false')
        except Exception,e:
            raise Exception("checkVideoListSize exception")
        
    def checkPhotoUrlSize(self):#测试获得图片地址urlList的长度，与预期长度是否相等
        try:
            beginTime = Config().getFromConfig(Constants.frame, "photo-begin-time")
            endTime = Config().getFromConfig(Constants.frame, "photo-end-time")
            type = Config().getFromConfig(Constants.frame, "type")
            urls = self.getUrlList(beginTime=beginTime,endTime=endTime,type=type)
            if urls!=None:
                if len(urls)==12:
                    log.debug('the result is success')
                else:
                    log.debug('the result is false')
        except Exception,e:
            raise Exception("checkPhotoUrlSize exception")
        
if __name__ == '__main__':
    print "begin DeviceManagementServer test."



