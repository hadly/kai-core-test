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
                    log.info("ֱ������URL��ַΪ:%s,������idΪ%s���豸��Ϣ����False",url,deviceId)
                    return False
                return True
            else:
                log.debug('msg: The Get Url is None~~')
                log.info("ֱ������URL��ַΪ�գ�False")
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
            log.debug(urls) 
            return urls
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception('getUrlList exception!')
    #here are some auxiliary methods
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
                log.info("��Ƶ�洢����URLΪ��,False")
                return False
        except Exception,e:
            log.error('Error:%s',e)
            return False
        
    def checkPhotoUrlSize(self):#���Ի��ͼƬ��ַurlList�ĳ��ȣ���Ԥ�ڳ����Ƿ����
        try:
            sessionId = str(uuid1())
            beginTime = Config().getFromConfigs(Constants.photoStrategy, "photo-begin-time-UTC")
            endTime = Config().getFromConfigs(Constants.photoStrategy, "photo-end-time-UTC")
            type = Config().getFromConfigs(Constants.photoStrategy, "type")
            urls = self.getUrlList(sessionId=sessionId,beginTime=beginTime,endTime=endTime,type=type)
            log.debug('urls size:%d',len(urls))
            if len(urls)>=18:#���ۻ����22��ͼ,�м����ڴ����ִ�У����Ի��ٵ�һЩ��������18��������Ϊ�ϸ�
                log.debug('the result is success')
                return True
            else:
                log.debug('the result is false')
                log.info("ͼƬ�洢����URL�Ĵ�СΪ%d,����Ԥ�ڵĴ�С��False",len(urls))
                return False
        except Exception,e:
            log.error('Error:%s',e)
            return False
