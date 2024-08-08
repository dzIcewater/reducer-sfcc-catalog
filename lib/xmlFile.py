from .file import File
import xml.etree.ElementTree as ET

# the json config file.  
class xmlFile(File):
    _rootElemID = ''
    rootTag = ''
    iterationTag = ''
    
    def __init__(self, fname,path, isOutFileBool, rootTag): 
        #super(configFile,self).__init__(self._name,self._path)
        super().__init__(fname, path, isOutFileBool)
        self.rootTag = rootTag
    
    # return None if none found
    def readOneElement(self, elemID):
        elem = []
        done=False
        dowrite=False
        self.eatSpaces()
        while (False == done):
            line = self._fh.readline()
            if '<'+elemID+' ' in line  or  '<'+elemID+'>' in line:
                dowrite=True
            if '</' + elemID + '>' in line:
                done=True
            if dowrite:
                elem.append(line)
        return elem
    
    def eatSpaces(self):
        done=False
        while (not done):
            line = self._fh.readline()
            if line.strip() == '\n':
                pass
            elif line.strip() == '':
                done = True
                return None
        return True #ok 
         
    def writeOneElement(self, elemArr):
        for line in elemArr:
            if self._isOutFileBool == True:
                self._fh.write(line)
            else:
                raise Exception('writeOneElement: file is not outfile')
        
        return 
    #get only the root elem. includes anything before it too like <xml... .   
    def readRootTag(self, elemID):
        self.initFileHandler()
        elem = []
        done=False
        while (False == done):
            line = self._fh.readline()
            elem.append(line)
            if '<'+elemID in line:
                done = True
        self.readRootElemOpeningTag = elem
        return elem
        
        
        
    
    def test1(self):
        self._rootElemID = 'catalog'
        re = self.readRootElemOpeningTag = self._rootElemID 
        id = 'header'
        e = self.readOneElement(id)
        a = e; 
        
    
         
              
        