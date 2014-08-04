'''
Created on 2014-7-17

@author: guanxingquan
'''
from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants,MysqlConnector
from RecordingCommsAPI import RecordingServerService
from arbiter.utils.Constants import deleteDevice,streamControl,frame
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
            self.deviceId = Config().getFromConfigs(deleteDevice,"device-id")
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
            beginTime = Config().getFromConfigs(Constants.frame, "liveview-begin-time-eight")
            chunkSize = Config().getFromConfigs(Constants.frame,"chunk-size")
            percent = Config().getFromConfigs(Constants.frame,"rates")
            frame_rate = Config().getFromConfigs(Constants.frame,"frame-rate")
            endTime = Config().getFromConfigs(Constants.frame, "liveview-end-time-eight")
            info = {"storage-type":"video-recording", "stream-type":"http/h264","begin":beginTime,"end":endTime}
            streamInfo = json.dumps(info)
            log.debug(streamInfo) 
            streamList = self.client.getStreamList((int)(self.deviceId),0,streamInfo)
            log.debug(streamList) 
            for stream in streamList:
                log.debug('*********************')
                strJson = json.loads(stream)
#                 log.debug('AAAAAAAAAAAAAAAAAAAAAAAAAA')
                begin = strJson["from"]
                end = strJson["to"]
                dur = strJson["dur"]
                fn = strJson["fn"]
                fps = strJson["fps"]
                size = strJson["size"]
                if fn!='0' and size!='0':
                    log.debug('fps:%s',fps)
                    if abs(eval(chunkSize)-eval(dur)/60)<=(eval(chunkSize)*eval(percent)) and abs(eval(frame_rate)-eval(fps))<=(eval(frame_rate)*eval(percent)):
                        log.info('this video from %s to %s is success',begin,end)
                    else:
                        log.info('this video from %s to %s is fail',begin,end)
                else:
                    log.info('this video"size from %s to %s is fail',begin,end)
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception('testGetVideoStreamList exception')
        
    def testGetPhotoStreamList(self):
        try:
            beginTime = Config().getFromConfigs(Constants.frame, "photo-begin-time-eight")
            endTime = Config().getFromConfigs(Constants.frame, "photo-end-time-eight")
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
                    log.info('the time:%s add a picture successed',start)
                else:
                    log.info('the test add a picture have an error at %s',start)       
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception('testGetPhotoStreamList exception')
        
    def testGetEventStreamList(self):
        try:
            log.debug('*******testGetEventStreamList begin******')
            eventId = Config().getFromConfigs(Constants.streamControl, "event-id")
            chunkSize = Config().getFromConfigs(Constants.frame,"chunk-size")
            percent = Config().getFromConfigs(Constants.frame,"percent")
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
                        log.info('Add an event success' )
                    else:
                        log.info('The result error is relatively large, so the failure')
                else:
                    log.debug('Add an event error,have zero value')
            log.debug('*******testGetEventStreamList end******')       
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception('testGetEventStreamList exception')
        