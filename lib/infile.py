from pathlib import Path
from .file import file

class infile(File):
    _isOutFileBool = False
    
    def __init__(self,fname,path,isOutFileBool):
        self._filename = fname
        self._path = path
        self._isOutFileBool = isOutFileBool
        self.setFullpath()
        self.initFileHandler()  #call again to open & reset pointer to start of file. 
        return self