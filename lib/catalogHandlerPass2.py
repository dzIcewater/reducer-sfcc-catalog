from .file import File
from lib.catalogOutFile import catalogOutFile
import xml.sax


class catalogHandlerPass2(xml.sax.ContentHandler):
    _reg = None
    _catalogOutFile = None
     
    def __init__(self, reg, catalogOutFile):
        self._reg = reg
        self._catalogOutFile = catalogOutFile
        self.currentProductXml = ''
        self.inProduct=None
        self.getCurrentProduct=None
        self.currentElemName = None
        self.currentElemAttrs = None
        self.currentElemContent = None
        self.lastEvent = None
    
    def startDocument(self):
        pass

    def endDocument(self):
        self._catalogOutFile.close()
        
    def startElement(self, name, attrs):
        self.currentElemName = name
        self.currentElemAttrs = attrs
        if self.currentElemName == 'product':
            self.inProduct = 1
            pid =  attrs['product-id']
            if pid in self._reg.dataHolder.masterCatProducts or pid in self._reg.dataHolder.variantProducts:
                self.getCurrentProduct = 1
        outputStr = '<'+name+''+self.getAttrsStr(attrs)+'>'
        self.writeStartElement(outputStr)
            
    def characters(self,content):
        self.currentElemContent = content
        self.writeCharacters(content)
        
    def endElement(self, name):
        self.writeEndElement('</' + name + '>')
        if name == 'product':
            self.inProduct = 0
            self.getCurrentProduct = 0
        self.currentElemName = None
        self.currentElemAttrs = None
        self.currentElemContent = None
        
        
    def getAttrsStr(self, attrs):
        o=' '
        for i, (k, v) in enumerate(attrs.items()):
            o += k+'="'+v+'" '
        return o       
    
    def writeStartElement(self,string):
        self.writeStr(string,'startElement')
    
    def writeCharacters(self,string):
        if '\n' not in string  and  string.strip() == string:
            self.writeStr(string,'characters')    
        elif string == '\n':
            self.writeStr(string,'characters')
        elif string.strip() == '' and '\n' not in string:
            z=1
        
    def writeEndElement(self,string):
        self.writeStr(string, 'endElement')
    
    #rules based on start, chars, or end elem. 
    #endelem: always write newline.
    #start: with chars after it:  no newline.   Else,  newline.
    #chars: always no newline
    def writeStr(self,string,eventType):
        if self.inProduct:
            if self.getCurrentProduct == 1:
                self.printStr( string )
            else:
                z=1 # do nothing!
            #else dont print it at all. 
        else:
            self.printStr(string)
           
         
    #write str only
    def printStr(self, data):
        if data.endswith('\n'):
            t=1
            if data.strip() == '':
                t=2
            
                if self.getCurrentProduct == 0:
                    t=4
                    if self.currentElemName == None:
                        t=5
        if data.endswith('\n') and data.strip() == '' and self.currentElemName == None:
            z=2
        else:
            self.outputPrint(data)
    #write str and then end of line.
    
    # output the data, to either terminal, or file; logic switch = todo here 
    def outputPrint(self, data):
        self._catalogOutFile.writeString(data)
        print(data)
         
    #not using now 
    def printStrLn(self, data):
        if(data.endswith('\n')):
            self.outputPrint( data )
        else:
            self.outputPrint( data + '\n' )