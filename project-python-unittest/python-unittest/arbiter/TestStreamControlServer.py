# -*- coding: GBK -*-
'''
Created on 2014-6-18

@author: lizhinian
'''
from CoreServices import StreamControlService
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants
from arbiter.utils.Constants import arbiter,streamControl,deleteDevice
from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils import LogUtil
import logging
from uuid import uuid1
import time

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
    
    def testLiveViewResultUrl(self):
        try:
            log.debug("test begin liveview")
            sessionId = str(uuid1())
            type = Config().getFromConfigs(Constants.videoStrategy, "type")
            deviceId = Config().getFromConfigs(deleteDevice, "device-id")
            urls = self.getUrlList(sessionId=sessionId,beginTime=None,endTime=None,type=type)
            if len(urls)!=0:
                url = urls[0]
            #the returned url is like--rtmp://10.101.0.206:1935/flvplayback/live13-0
                log.debug("liveview,deviceId=%s, urls=%s, url=%s",deviceId,urls,url)
                if deviceId not in url:
                    log.debug('liveview url not normal,false')
                    log.info("liveview URL is %s, no deviceId %s found in it. False",url,deviceId)
                    return False
                return True
            else:
                log.debug('msg: The Get Url is None~~')
                log.info("liveview URL is empty. False")
                return False
        except Exception, e:
            log.error("liveview Error:%s",e)
            return False
    
    def testBeginPlayBack(self):
        pass
         
    def getUrlList(self,sessionId,beginTime,endTime,type):
        try:
            ttl = (long)(Config().getFromConfigs(Constants.streamControl, "ttl"))
            channelId = Config().getFromConfigs(Constants.streamControl, "channel-id")
            deviceId = Config().getFromConfigs(Constants.deleteDevice, "device-id")
            urls = self.client.beginStreamSession(sessionId, ttl, type,None,deviceId, channelId, beginTime, endTime)
            log.debug('url list=%s', urls) 
            return urls
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception('getUrlList exception!')

    def controlSession(self):
        try:
            sessionId = str(uuid1())
            type = Config().getFromConfigs(Constants.videoStrategy, "type")
            self.getUrlList(sessionId, None, None, type)
            time.sleep(50)
            result = Mysql().getStreamSessionInfoBySessionId(sessionId)
            if len(result) > 0:
                self.client.keepStreamSessionAlive(sessionId,120,None)
            else:
                log.info("sessionId : %s not in stream_session_info",sessionId)
                return -1
            time.sleep(65)
            keepresult = Mysql().getStreamSessionInfoBySessionId(sessionId)
            if len(keepresult) > 0:
                log.info("keepSession                             OK")
                self.client.endStreamSession(sessionId)
                time.sleep(5)
                endresult = Mysql().getStreamSessionInfoBySessionId(sessionId)
                if len(endresult) == 0:
                    log.info("endSession                              OK")
                    return 1
                else:
                    log.info("endSession                              False")
                    return -1
            else:
                log.info("keepSession                             False")
                return -1
        except Exception,e:
            log.error('Error:%s',e)
            return -1

    def checkVideoListSize(self):
        try:
            sessionId = str(uuid1())
            beginTime = Config().getFromConfigs(Constants.videoStrategy, "liveview-begin-time-UTC")
            endTime = Config().getFromConfigs(Constants.videoStrategy, "liveview-end-time-UTC")
            type = Config().getFromConfigs(Constants.videoStrategy, "type")
            urls = self.getUrlList(sessionId=sessionId,beginTime=beginTime,endTime=endTime,type=type)
            log.debug('urls:%s',urls)
            
            if len(urls)==1:
                log.debug('the result is success')
                return True
            else:
                log.debug('the result is false')
                log.info("liveview URL is empty, False")
                return False
        except Exception,e:
            log.error('Error:%s',e)
            return False
        
    def checkPhotoUrlSize(self):#测试获得图片地址urlList的长度，与预期长度是否相等
        try:
            sessionId = str(uuid1())
            beginTime = Config().getFromConfigs(Constants.photoStrategy, "photo-begin-time-UTC")
            endTime = Config().getFromConfigs(Constants.photoStrategy, "photo-end-time-UTC")
            type = Config().getFromConfigs(Constants.photoStrategy, "type")
            urls = self.getUrlList(sessionId=sessionId,beginTime=beginTime,endTime=endTime,type=type)
            log.debug('urls size:%d',len(urls))
            
            if len(urls)>=18:#理论会产生22张图,中间由于代码的执行，所以会少掉一些，所以在18张以上视为合格
                log.debug('the result is success')
                return True
            else:
                log.debug('the result is false')
                log.info("image recording URL size is %d, not as expected. False",len(urls))
                return False
        except Exception,e:
            log.error('Error:%s',e)
            return False
