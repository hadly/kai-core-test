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
            endTime = Config().getFromConfig(Constants.streamControl, "liveview-end-time")
            info = {"begin":beginTime,"end":endTime}
            streamInfo = json.dump(info)
            streamList = self.client.getStreamList(self.deviceId,0,streamInfo)
            for stream in streamList:
                pass        #never end,please wait 
        except Exception,e:
            raise Exception('testGetVideoStreamList exception')
        
    def testGetPhotoStreamList(self):
        try:
            beginTime = Config().getFromConfig(Constants.frame, "photo-begin-time")
            endTime = Config().getFromConfig(Constants.frame, "photo-end-time")
            info = {"begin":beginTime,"end":endTime}
            streamInfo = json.dump(info)
            streamList = self.client.getStreamList(self.deviceId,0,streamInfo)
            for stream in streamList:
                pass        #never end,please wait 
        except Exception,e:
            raise Exception('testGetPhotoStreamList exception')