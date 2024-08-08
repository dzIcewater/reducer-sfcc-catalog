from pathlib import Path

class File(object):
    _filename = 'uninit'
    _path = 'uninit'
    _fh = 'uninit'
    _fullpathObj  = None  # this is the Path object. 
    _isOutFileBool = False
 
    def __init__(self,fname,path,isOutFileBool):
        self._filename = fname
        self._path = path
        self._isOutFileBool = isOutFileBool
        self.setFullpath()
        self.initFileHandler()  #call again to open & reset pointer to start of file. 
        
    
    def setAsWritable(self):
        self._isOutFileBool = True
    
    def setAsReadable(self):
        self._isOutFileBool = False
        
    def getFileHandler(self):
        return self._fh
        
    def printname(self):
        print(self._filename);
    
    def setFullpath(self):
        pathObj = Path(self._path)
        self._fullpathObj = pathObj / self._filename
        # self._fullpathObj = Path(self._path + '/' + self._filename) #old way not doing anymore

    def initToWrite(self):
        self.setAsWritable()
        self.initFileHandler()
        
    def initToRead(self):
        self.setAsReadable()
        self.initFileHandler()

    def initFileHandler(self):
        flag = 'r' # write new file
        if self._isOutFileBool == True:
            flag = 'w'
            pathobjfile = Path(self._fullpathObj)
            if pathobjfile.exists() == False:
                pathobjfile.touch()
                    
        self._fh = open( self._fullpathObj , flag)
    
    def close(self):
        self._fh.close()
    
    def flush(self):
        self._fh.flush()
        
    def peekLine(self):
        pos = self._fh.tell()
        line = self._fh.readline()
        self._fh.seek(pos)
        return line
    
    def writeString(self,string):
        self._fh.write(string)
        