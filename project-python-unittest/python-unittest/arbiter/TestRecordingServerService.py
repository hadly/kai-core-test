'''
Created on 2014-7-17

@author: guanxingquan
'''
from arbiter.utils.MysqlOperator import Mysql
from arbiter.utils.ConfigurationReader import Config
from arbiter.utils import ThriftClient, Constants,MysqlConnector
from RecordingCommsAPI import RecordingServerService
import logging
import json
from arbiter.TestRecordingServerService import log
log = logging.getLogger('TestRecordingServerService')
class RecordingServerService():
    client = None 
    con = None
    def __init__(self):
        try:
            self.con = MysqlConnector.getConnection()
            self.deviceId = Config().getFormConfig(Constants.deleteDevice,"device-id")
            rsServerInfo = Mysql(self.con).getRsServerInfo(self.deviceId)
            host = dsServerInfo[0][1]
            port = dsServerInfo[0][2]
            self.client = ThriftClient.getThriftClient(host, port, RecordingServerService)
        except Exception,e:
            raise Exception('RecordingServerService __init__ exception')
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
        
    def testGetVideoStreamList(self):
        try:
            beginTime = Config().getFromConfig(Constants.streamControl, "liveview-begin-time")
            chunkSize = Config().getFromConfig(Constants.frame,"chunk-size")
            percent = Config().getFromConfig(Constants.frame,"percent")
            frame_rate = Config().getFromConfig(Constants.frame,"frame-rate")
            endTime = Config().getFromConfig(Constants.streamControl, "liveview-end-time")
            info = {"storage-type":"video-recording", "stream-type":"http/h264","begin":beginTime,"end":endTime}
            streamInfo = json.dump(info)
            streamList = self.client.getStreamList(self.deviceId,0,streamInfo)
            for stream in streamList:
                strJson = json.loads(stream)
                begin = strJson["from"]
                end = strJson["to"]
                dur = strJson["dur"]
                fn = strJson["fn"]
                fps = strJson["fps"]
                size = strJson["size"]
                if fn!='0' and size!='0':
                    if abs(eval(chunkSize-dur))<=eval(chunkSize*percent) and abs(eval(frame_rate-fps))<=eval(frame_rate*percent):
                        log.debug('this video from %s to %s is success',begin,end)
                    else:
                        log.debug('this video from %s to %s is fail',begin,end)
                else:
                    log.debug('this video from %s to %s is fail',begin,end)
        except Exception,e:
            raise Exception('testGetVideoStreamList exception')
        
    def testGetPhotoStreamList(self):
        try:
            beginTime = Config().getFromConfig(Constants.frame, "photo-begin-time")
            endTime = Config().getFromConfig(Constants.frame, "photo-end-time")
            info = {"storage-type":"image-recording", "stream-type":"http/jpeg","begin":beginTime,"end":endTime}
            streamInfo = json.dump(info)
            streamList = self.client.getStreamList(self.deviceId,0,streamInfo)
            for stream in streamList:
                strJson = json.load(stream)
                start = strJson['time']
                width = strJson['width']
                height = strJson['height']
                size = strJson['size']
                if eval(width*height*size)!=0:
                    log.debug('the time:%s add a picture successed',start)
                else:
                    log.debug('the test add a picture have an error at %s',start)       
        except Exception,e:
            raise Exception('testGetPhotoStreamList exception')
        
    def testGetEventStreamList(self):
        try:
            eventId = Config().getFromConfig(Constants.streamControl, "event-id")
            chunkSize = Config().getFromConfig(Constants.frame,"chunk-size")
            percent = Config().getFromConfig(Constants.frame,"percent")
            info = {"storage-type":"event-recording", "stream-type":"http/h264", "event-id":eventId}
            streamInfo = json.dump(info)
            streamList = self.client.getStreamList(self.deviceId,0,streamInfo)
            for stream in streamList:
                strJson = json.load(stream)
                dur = strJson['dur']
                fn = strJson['fn']
                fps = strJson['fps']
                size = strJson['size']
                if eval(fps*fn*size)!=0:
                    if abs(eval(chunkSize-dur))<=eval(chunkSize*percent):
                        log.debug('Add an event success' )
                    else:
                        log.debug('The result error is relatively large, so the failure')
                else:
                    log.debug('Add an event error,have zero value')       
        except Exception,e:
            raise Exception('testGetEventStreamList exception')