'''
Created on 2014-6-19

@author: Administrator
'''
import ConfigParser

configFile = "configuration.cfg"
class Config():
    config = None
    def __init__(self):
        #open file
        self.config = ConfigParser.ConfigParser()
        cfgfile = open(configFile,'r')
        self.config.readfp(cfgfile) 

    def getConfig(self):
        return self.config
    
    def getFromConfig(self, section, key):
        return self.config.get(section, key)
        
    def getFromConfigs(self, section, key):
        return self.config.get(section, key)
    
    def writeToConfig(self, section, key, value):
        self.config.set(section, key, value)
        self.config.write(open(configFile,'w'))
     
if __name__ == '__main__':
        #write the file as following
        configuration = Config()
        config = configuration.getConfig()
        config.set('deleteDevice','deviceId','56')
        configuration.writeToConfig()
        