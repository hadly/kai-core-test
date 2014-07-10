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
            sessionId = Config().getFromConfig(Constants.streamControl, "session-id")
            ttl = (long)(Config().getFromConfig(Constants.streamControl, "ttl"))
            type = Config().getFromConfig(Constants.streamControl, "type")
            beginTime = Config().getFromConfig(Constants.streamControl, "liveview-begin-time")
            endTime = Config().getFromConfig(Constants.streamControl, "liveview-end-time")
            channelId = Config().getFromConfig(Constants.streamControl, "channel-id")
            deviceId = Config().getFromConfig(Constants.deleteDevice, "device-id")
            urls = self.client.beginStreamSession(sessionId, ttl, type, None, deviceId, channelId, beginTime, endTime)
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
        
    
    
    
    
    #here are some auxiliary methods


if __name__ == '__main__':
    print "begin DeviceManagementServer test."



