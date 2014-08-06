'''
Created on 2014-7-17

@author: guanxingquan
'''
from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants,MysqlConnector
from RecordingCommsAPI import RecordingServerService
# from arbiter.utils.Constants import deleteDevice,streamControl
import logging
import json
import time
log = logging.getLogger('TestRecordingServerService')
class RecordingServerServiceClient():
    client = None 
    con = None
    def __init__(self):
        try:
            self.con = MysqlConnector.getConnection()
            self.deviceId = Config().getFromConfigs(Constants.deleteDevice,"device-id")
            rsServerInfo = Mysql(self.con).getRsServerInfo(self.deviceId)
            if len(rsServerInfo)!=0:
                host = rsServerInfo[0][1]
                port = rsServerInfo[0][2]
                self.client = ThriftClient.getThriftClient(host, port, RecordingServerService)
        except Exception,e:
            log.error('RecordingServerService error:%s',e)
            raise Exception('RecordingServerService __init__ exception')
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
        
    def testGetVideoStreamList(self):
        try:
            num = 0
            beginTime = Config().getFromConfigs(Constants.videoStrategy, "liveview-begin-time-local")
            chunkSize = Config().getFromConfigs(Constants.configControl,"chunk-size")
            percent = Config().getFromConfigs(Constants.deviceFrameRate,"rates")
            frame_rate = Config().getFromConfigs(Constants.deviceFrameRate,"frame-rate")
            endTime = Config().getFromConfigs(Constants.videoStrategy, "liveview-end-time-local")
            info = {"storage-type":"video-recording", "stream-type":"http/h264","begin":beginTime,"end":endTime}
            streamInfo = json.dumps(info)
            log.debug(streamInfo) 
            streamList = self.client.getStreamList((int)(self.deviceId),0,streamInfo)
            log.debug(streamList) 
            for stream in streamList:
                log.debug('*********************')
                strJson = json.loads(stream)
                begin = strJson["from"]
                end = strJson["to"]
                dur = strJson["dur"]
                fn = strJson["fn"]
                fps = strJson["fps"]
                size = strJson["size"]
                if fn!='0' and size!='0':
                    log.debug('fps:%s',fps)
                    if abs(eval(chunkSize)-eval(dur)/60)<=(eval(chunkSize)*eval(percent)) and abs(eval(frame_rate)-eval(fps))<=(eval(frame_rate)*eval(percent)):
                        log.debug('this video from %s to %s is success',begin,end)
                        num += 1
                    else:
                        log.debug('this video from %s to %s is fail',begin,end)
                else:
                    log.debug('this video"size from %s to %s is fail',begin,end)
            if num == 4:
                return True
            return False
        except Exception,e:
            log.error('Error:%s',e)
            return False
        
    def testGetPhotoStreamList(self):
        try:
            num = 0
            beginTime = Config().getFromConfigs(Constants.photoStrategy, "photo-begin-time-local")
            endTime = Config().getFromConfigs(Constants.photoStrategy, "photo-end-time-local")
            info = {"storage-type":"image-recording", "stream-type":"http/jpeg","begin":beginTime,"end":endTime}
            streamInfo = json.dumps(info)
            streamList = self.client.getStreamList((int)(self.deviceId),0,streamInfo)
            for stream in streamList:
                strJson = json.loads(stream)
                start = strJson['time']
                width = strJson['width']
                height = strJson['height']
                size = strJson['size']
                if eval(width)*eval(height)*eval(size)!=0:
                    log.debug('the time:%s add a picture successed',start)
                    num += 1
                else:
                    log.debug('the test add a picture have an error at %s',start)
            if num == 12:
                return True
            return False
        except Exception,e:
            log.error('Error:%s',e)
            return False
        
    def testGetEventStreamList(self):
        try:
            log.debug('*******testGetEventStreamList begin******')
            eventId = Config().getFromConfigs(Constants.streamControl, "event-id")
            chunkSize = Config().getFromConfigs(Constants.configControl,"chunk-size")
            percent = Config().getFromConfigs(Constants.deviceFrameRate,"percent")
            info = {"storage-type":"event-recording", "stream-type":"http/h264", "event-id":eventId}
            streamInfo = json.dumps(info)
            log.debug('%s',self.client)
            streamList = self.client.getStreamList(int(self.deviceId),0,streamInfo)
            log.debug('streamList:%s',streamList)
            for stream in streamList:
                strJson = json.loads(stream)
                dur = strJson['dur']
                fn = strJson['fn']
                fps = strJson['fps']
                size = strJson['size']
                if eval(fps)*eval(fn)*eval(size)!=0:
                    if abs(eval(chunkSize)-eval(dur)/60)<=eval(chunkSize*percent):
                        log.debug('Add an event success' )
                        return True
                    else:
                        log.debug('The result error is relatively large, so the failure')
                        return False
                else:
                    log.debug('Add an event error,have zero value')
                    return False
            log.debug('*******testGetEventStreamList end******')       
        except Exception,e:
            log.error('Error:%s',e)
            return False
        