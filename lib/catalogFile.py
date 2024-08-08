from .xmlFile import xmlFile

#  catalog file, in or out either. based on  isOutFileBool param.  
class catalogFile(xmlFile):
    
    def __init__(self, fname,path, isOutFileBool):
        super().__init__(fname, path, isOutFileBool, 'catalog')
        self.iterationTag = 'product'
       
    def test1(self):
         
        pass