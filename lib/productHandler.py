import xml.sax

#  catalog file, in or out either. 
class productHandler(xml.sax.ContentHandler):
    
    
    def __init__(self):
        pass
    
    def startElement(self, name, attrs):
        self.currentElem = name
        if name != 'product':
            raise Exception("err, producthandler: first elem not a product! name: " + name)
        
    def characters(self,content):
        
        self.content = content
        
    def endElement(self, name):
        # print('elem was: ' + self.currentElem)
        self.currentElem = ''
        