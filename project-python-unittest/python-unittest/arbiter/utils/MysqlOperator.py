'''
Created on 2014-6-20

@author: Administrator
'''
from Constants import addedDeviceName
from arbiter.utils import MysqlConnector

class Mysql(object):
    
    con = None
    def __init__(self, mysqlConnection):
        '''
        Constructor
        '''
        self.con = MysqlConnector.getConnection()
    
    def executeSql(self, sql, *params):
        cur =self.con.cursor()
        num = cur.execute(sql,params)
        self.con.commit()
        result = cur.fetchall()
        return result
        
    def getDevice(self):
        sql = "select * from devices where name=%s ;"
        result = self.executeSql(sql, addedDeviceName)
        return result
        
    def getDsDeviceInfo(self, deviceId):
        sql = "select * from ds_device_info where id=%s ;"
        result = self.executeSql(sql, deviceId)
        return result
    
    def getDsServerInfo(self,deviceId):
        sql = "select * from ds_server_info where id=(select server_id from ds_device_info where id=%s) ;"
        result = self.executeSql(sql,deviceId)
        return result
    
    def getRsServerInfo(self,deviceId):
        sql = "select * from rs_server_info where id=(select server_id from rs_device_info where id=%s) ;"
        result = self.executeSql(sql,deviceId)
        return result
    
    def cleanDeviceInfo(self, deviceId):
        cur =self.con.cursor()
        sql1 = "delete from device_events where device_id=%s ;"
        sql2 = "delete from ds_device_info where id=%s ;"
        sql3 = "delete from devices where id=%s ;"
        
        num = cur.execute(sql1, deviceId)
        num = cur.execute(sql2, deviceId)
        num = cur.execute(sql3, deviceId)
        self.con.commit()
        result = cur.fetchall()
        return result
            
    def getChannelDeviceMap(self):
        sql = "select * from channel_device_map;"
        result = self.executeSql(sql)
        return result
        
    def getStreamSessionInfo(self, deviceId):
        sql = "select * from stream_session_info where device_id=%s ;"
        result = self.executeSql(sql, deviceId)
        return result
        
        
        
        