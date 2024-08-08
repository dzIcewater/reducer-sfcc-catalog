from .file import File
from lib.catalogOutFile import catalogOutFile

#  catalog file, in or out either.
class inventoryHandlerPass1( ):
   
    outFile = None
    reg = None
    multiFiles  = None
    listid1,listid2,listid3 = None,None,None
    part1 = """<?xml version="1.0" encoding="UTF-8"?>
<inventory xmlns="http://www.demandware.com/xml/impex/inventory/2007-05-31">
    <inventory-list>
        <header list-id="{listid}">
            <default-instock>false</default-instock>
            <description>site DW Inventory</description>
            <use-bundle-inventory-only>false</use-bundle-inventory-only>
            <on-order>false</on-order>
        </header>
        <records>
      """
      
    part2 = """</records>
    </inventory-list>
</inventory>
    """
    
    def __init__(self, reg ):
        self.reg = reg
        self.outFileGlobal = File(reg.configJson.data['inventoryOutGlobal'],'outfiles', True )
        self.outFileEast = File(reg.configJson.data['inventoryOutEast'], 'outfiles', True)
        self.outFileWest = File(reg.configJson.data['inventoryOutWest'], 'outfiles', True)
        self.multiFiles = [self.outFileGlobal, self.outFileEast, self.outFileWest]
        self.listid1 =   self.reg.configJson.data['main-site-id'] 
        self.listid2 =   self.reg.configJson.data['east-site-id']  
        self.listid3 =   self.reg.configJson.data['west-site-id']   


    def writeAllForAllInventoryLists(self):
        reg = self.reg
        outFileGlobal = self.outFileGlobal
        # outFileGlobal.writeString(self.part1)
        # self.writeStringToMultiFiles(self.part1)
        self.writePart1ToMultiFiles()
        for sku in reg.dataHolder.masterCatProducts.keys():
            v = self.getSkuRecord(sku)
            #outFileGlobal.writeString( self.getSkuRecord(sku))
            self.writeStringToMultiFiles(self.getSkuRecord(sku))
        for sku in reg.dataHolder.variantProducts.keys():
            v = self.getSkuRecord(sku)
            # outFileGlobal.writeString( self.getSkuRecord(sku))
            self.writeStringToMultiFiles(self.getSkuRecord(sku))
        # outFileGlobal.writeString(self.part2)
        self.writeStringToMultiFiles(self.part2)
        outFileGlobal.flush()
        outFileGlobal.close()
        
        
    def getPart1String(self, myListID):
        return self.part1.format(listid=myListID)
        
    def writeStringToMultiFiles(self, string):
        for f in self.multiFiles:
            f.writeString(string)
   
    def writePart1ToMultiFiles(self):
        s1 = self.getPart1String(self.listid1)
        self.multiFiles[0].writeString(s1)
        s2 = self.getPart1String(self.listid2)
        self.multiFiles[1].writeString(s2)
        s3 = self.getPart1String(self.listid3)
        self.multiFiles[2].writeString(s3)
        
        
    def getSkuRecord(self, sku):
        return """
            <record product-id="{skuid}">
                <allocation>1234</allocation>
                <perpetual>true</perpetual>
                <preorder-backorder-handling>none</preorder-backorder-handling>
                <preorder-backorder-allocation>1234</preorder-backorder-allocation>
                <ats>1234</ats>
                <on-order>1234</on-order>
                <turnover>1234</turnover>
            </record>
  
        """.format(skuid=sku)
        
        
    
        
        
    