from .file import File
from lib.configFile import configFile
from lib.catalogInFile import catalogInFile
from lib.catalogOutFile import catalogOutFile
from lib.filters import filters
from lib.dataHolder import dataHolder



class registry(object):
    configJson = None
    catInFile = None
    catOutFile = None
    dataHolder = None
    masterCatalogReducer = None
    siteCatalogOperationsObj = None
    remainingRequiredMastersList = []
    DEBUG = 0
    
    def __init__(self):
        print('load configfile')
        self.configJson = configFile()
        self.DEBUG = self.configJson.data['DEBUGFLAG']
        isOutFlag = False
        self.catInFile = catalogInFile( self.configJson.data['catalog'] , self.configJson.data['infilesDir'] ) 
        isOutFlag = True
        self.catOutFile = catalogOutFile( self.configJson.data['catalogOut'], self.configJson.data['outfilesDir'] )
        self.filters = self.configJson.data['filters']
        self.dataHolder = dataHolder(self)
        for masterSKU in self.configJson.data['REQUIREDMASTERS']:
            self.remainingRequiredMastersList.append(masterSKU)
    
    def variantCountWithinMaxVariantCountPerMaster(self, count):
        if count <= self.configJson.data['MAXVARIANTCOUNTPERMASTER']:
            return True
        return False
     
    def requiredMastersAllFound(self):
        
        return False   
    
    #
    def markRequiredMasterAsFound(self, masterSKU):
        if masterSKU in self.remainingRequiredMastersList:
            remainingRequiredMastersList.remove(masterSKU)
        else:
            raise Exception('mastersku not found in remainingRequiredMastersList!')

 