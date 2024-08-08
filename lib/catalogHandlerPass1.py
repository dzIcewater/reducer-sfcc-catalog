import xml.sax
import os 
from pathlib import Path

#  catalog file, in or out either. 

#TODO:    availableForInStorePickup as a custom attr required to be true for some of the master skus   maybe
class catalogHandlerPass1(xml.sax.ContentHandler):
    filters=None
    reg = None
    _fhPathObj = None
    _fh = None
    filesProcessedCount = None
    _fhSize = None
    _DISABLEFILTERBool = False
    
    def __init__(self, reg, fhPathObj, DISABLEFILTERBool=False):
        self.reg = reg
        self._fhPathObj = fhPathObj
        self._DISABLEFILTERBool = DISABLEFILTERBool 
        self._fhSize = Path(self._fhPathObj).stat().st_size
        self._fh = self._fhPathObj.open()     #filehandler of the file we are parsing.  just use this to get size and print % of of it that we have parsed. 
        
        self.inProduct = 0
        self.inVariations = 0
        self.inVariants = 0
        self.productOnlineFlag = 0
        self.productOnlineFlagUq = 0
        self.productSearchableFlag = 0
        self.filesProcessedCount = 0
    
    def getFileHandler(self):
        return self._fh
        
    def startElement(self, name, attrs):
        self.currentElem = name
        self.currentElemAttrs = attrs
        if self.currentElem == 'product':
            self.inProduct = 1
            self.currentProductAttrs = attrs
            self.productVariantCount=0
            self.inVariations=0
            self.inVariationsVariants=0
            self.variants = []
            if attrs['product-id'] == '072937':
                z=1
                
        elif self.inProduct == 1 and name == 'variations':
            self.inVariations=1
        elif self.inVariations==1 and name == 'variants':
            self.inVariants = 1
            
    def characters(self,content):
        self.currentElemContent = content
        
    def endElement(self, name):
        if self.inProduct == 1:  #in product chunk, so check filter
            if name == 'product':           
                datapacket = self.doesPassFilter() #returns datapacket with categoryAssignmentID, or else a True/False for passed filter or not. 
                if datapacket != False: #this means filter result is True.
                    self.reg.dataHolder.masterCatProductAppend(self.currentProductAttrs['product-id'])
                    self.reg.dataHolder.allVariantProductsAppendGroup(self.variants)
                    if(type(datapacket) is dict  and 'categoryAssignmentID' in datapacket):
                        categoryAssignmentID = datapacket['categoryAssignmentID']
                        self.reg.dataHolder.chosenCategoryAppend(categoryAssignmentID)  # not need:  , self.currentProductAttrs['product-id']
                    k1 = self.reg.dataHolder.masterCatProducts.keys()          
                    k2 =  self.reg.dataHolder.variantProducts.keys()      
                     
                    if len(self.reg.dataHolder.masterCatProducts.keys()) + len(self.reg.dataHolder.variantProducts.keys()) > self.reg.configJson.data['MAXPRODUCTCOUNT'] :
                        #CAPPED OUT ON PRODUCTS, TIME TO EXIT. 
                        self._fh.close()
                        raise Exception('MAXPRODUCTCOUNT limit reached:  ' + str(self.reg.configJson.data['MAXPRODUCTCOUNT'])) 
                
                self.inProduct = 0                
                self.productOnlineFlag = 0
                self.productOnlineFlagUq = 0
                self.productSearchableFlag = 0
                self.variants = []
                self.currentProductAttrs = None
                self.filesProcessedCount += 1
                if self.filesProcessedCount % 5000 == 0:
                    progressPerc = self._fh.tell() / self._fhSize    #report progress intermittently
                    print('catalogHandlerPass1: progress Percent of entire mastercatalog file: ' + str ( progressPerc * 100))
        
            elif name == 'online-flag':
                
                if self.currentElemContent == 'true':
                    
                    if 'site-id' not in self.currentElemAttrs:
                        z3=3
        
            if name == 'online-flag' and self.currentElemContent == 'true' and 'site-id' in self.currentElemAttrs and self.currentElemAttrs['site-id'] == self.reg.configJson.data['site-id']:    
                self.productOnlineFlagUq = 1
            if name == 'online-flag' and self.currentElemContent == 'true' and 'site-id' not in self.currentElemAttrs:
                self.productOnlineFlag = 1
            if name == 'searchable-flag' and self.currentElemContent == 'true':
                self.productSearchableFlag = 1
                
            if name == 'variations':
                self.inVariations=0
            elif self.inVariations==1 and name == 'variants':
                self.inVariants = 0
            elif self.inVariants == 1 and name == 'variant':
                self.variants.append( self.currentElemAttrs['product-id'] )  #keeping track of the master's variants here. 
                
                
            # <online-flag>true</online-flag>
            # <online-flag site-id="mysiteid">true</online-flag>
            # <searchable-flag>true</searchable-flag>
    
    
    # inspect   currentElem   content   currentAttrs
    #out:
    def doesPassFilter(self):
        if( self._DISABLEFILTERBool == True):
            return True
        #1. is master: has at least 1 variant 
        #2. is master online true
        #3. is master searchable true     ok
        #4. is master in an online category   ok
        #TODO:   productOnlineFlagUq - decide what to do with this. 
        a1,a2,a3,a4 = 0,0,0,0 #debug 
        variants = self.variants
        countReqs=0
        if self.productOnlineFlag == 1:
            productOnline=1
            a1=1
            countReqs+=1
        if self.productSearchableFlag ==1:
            productSearchable=1
            a2=1
            countReqs+=1
        if len(self.variants) > 0:
            productHasVariants=1
            a3=1
            countReqs+=1
        # if self.reg.dataHolder.productSkuInOnlineCategory(self.currentProductAttrs['product-id']):
        #     productInOnlineCat=1
        #     countReqs+=1
        pid = self.currentProductAttrs['product-id']
         
        #myres = self.reg.dataHolder.productSkuInOnlineCategory(self.currentProductAttrs._attrs['product-id'])
             
        if (self.productOnlineFlag == 1 and self.productSearchableFlag == 1 and len(self.variants) > 0): #  or  self.currentProductAttrs._attrs['product-id'] in self.reg.configJson['REQUIREDMASTERS']:
            categoryAssignmentID = self.reg.dataHolder.getProductSkuOnlineCategoryAssignmentID(self.currentProductAttrs._attrs['product-id'])
            if categoryAssignmentID is not False:
                return {'categoryAssignmentID': categoryAssignmentID}
         
                            # 072937 is the test: 
                            #  sitecat 
                            #         <category-assignment category-id="about-3d-knit" product-id="072937"/>
                            # <category category-id="about-3d-knit">
                            #     <online-flag>true</online-flag>
                            #     <online-from>2020-02-26T14:00:00.000Z</online-from>
                            # <category-assignment category-id="about-3d-knit" product-id="072937"/>

        
        
        if countReqs == 1:
            b=1
        if countReqs ==2:
            b=2
        if countReqs == 3:
            b=3
        if countReqs==4:
            b=4
        
        return False
    
    def appendFilteredProduct(self, productStr):
        pass
    
    def getFilteredProducts(self):
        return self.filteredProducts
        
