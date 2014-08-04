# -*- coding: GBK -*-
'''
Created on 2014-6-18

@author: lizhinian
'''
from CoreServices import StreamControlService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants
from arbiter.utils.Constants import arbiter,streamControl,deleteDevice
from arbiter.utils import LogUtil
import logging
from uuid import uuid1

log = logging.getLogger("TestStreamControlServer")
class StreamControlServerClient():
    client = None 
    
    def __init__(self):
        try:
            host = Config().getFromConfigs(arbiter, "arbiter-server-host")
            port = Config().getFromConfigs(arbiter, "stream-control-server-port")
            self.client = ThriftClient.getThriftClient(host, port, StreamControlService)
        except Exception, e:
            log.error("StreamControlServer setup Error:%s",e)
            raise Exception("StreamControlServer setup error")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
    
    def testLiveViewResult(self):
        try:
            log.debug("test begin liveview")
            sessionId = Config().getFromConfigs(Constants.streamControl, "session-id")
            type = Config().getFromConfigs(streamControl, "type")
            deviceId = Config().getFromConfigs(deleteDevice, "device-id")
            urls = self.getUrlList(sessionId=sessionId,beginTime=None,endTime=None,type=type)
            log.debug('msg%s',urls)
            if len(urls)!=0:
                url = urls[0]
            #the returned url is like--rtmp://10.101.0.206:1935/flvplayback/live13-0
                log.debug("liveview,deviceId=%s, urls=%s, url=%s",deviceId,urls,url)
                if deviceId not in url:
                    log.info('liveview url not normal,false')
                    raise Exception("liveview url not normal")
                log.info("liveview can be played successfully")
            else:
                log.info('msg: The Get Url is None~~')
        except Exception, e:
            log.error("liveview Error:%s",e)
            raise Exception("liveview exception")
    
    def testBeginPlayBack(self):
        pass
         
    def getUrlList(self,sessionId,beginTime,endTime,type):
        try:
            ttl = (long)(Config().getFromConfigs(Constants.streamControl, "ttl"))
            channelId = Config().getFromConfigs(Constants.streamControl, "channel-id")
            deviceId = Config().getFromConfigs(Constants.deleteDevice, "device-id")
#             print self.client
#             log.debug('msg:time begin')
            urls = self.client.beginStreamSession(sessionId, ttl, type,None,deviceId, channelId, beginTime, endTime)
#             log.debug('msg:time end')
            log.debug(urls) 
            return urls
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception('getUrlList exception!')
    #here are some auxiliary methods
    def checkVideoListSize(self):
        try:
            sessionId = str(uuid1())
            print sessionId
            beginTime = Config().getFromConfigs(Constants.streamControl, "liveview-begin-time")
            endTime = Config().getFromConfigs(Constants.streamControl, "liveview-end-time")
            type = Config().getFromConfigs(Constants.streamControl, "type")
            urls = self.getUrlList(sessionId=sessionId,beginTime=beginTime,endTime=endTime,type=type)
            log.debug('urls:%s',urls)
            if len(urls)==1:
                log.info('the result is success')
            else:
                log.info('the result is false')
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception("checkVideoListSize exception")
        
    def checkPhotoUrlSize(self):#测试获得图片地址urlList的长度，与预期长度是否相等
        try:
            sessionId = str(uuid1())
            beginTime = Config().getFromConfigs(Constants.frame, "photo-begin-time")
            endTime = Config().getFromConfigs(Constants.frame, "photo-end-time")
            type = Config().getFromConfigs(Constants.frame, "type")
            urls = self.getUrlList(sessionId=sessionId,beginTime=beginTime,endTime=endTime,type=type)
            if len(urls)==12:
                log.info('the result is success')
            else:
                log.info('the result is false')
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception("checkPhotoUrlSize exception")
        
if __name__ == '__main__':
    print "begin DeviceManagementServer test."



