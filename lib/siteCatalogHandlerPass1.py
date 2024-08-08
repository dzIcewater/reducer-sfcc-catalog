import xml.sax

#  get all online categories in sitecatalog. 
class siteCatalogHandlerPass1(xml.sax.ContentHandler):
    filters=None
    reg = None        #class var, not instance
     
    
    def __init__(self , reg):
        self.reg = reg
        #self.filters = reg.getFilters() #not used yet
        self.inCategory=0     #instance vars. 
        self.inCategoryAssignment=0
        self.currentElemAttrs = None
        self.currentCategoryAttrs = None
        self.currentCategoryParent = None
        self.currentElemContent = ''
        
    def startElement(self, name, attrs):
        self.currentElem = name
        self.currentElemAttrs = attrs
        self.currentElemContent = ''
        if name == 'category':
            self.inCategory = 1
            self.categoryOnlineFlag = 0
            #attrs['category-id']allCategoryAppend
            self.currentCategoryAttrs = attrs
            if self.currentCategoryAttrs['category-id'] == 'women-travel-shop-lightweight-layers':
                s = 1
        elif name == 'category-assignment':
            catid = attrs['category-id']
            pid = attrs['product-id']
            self.reg.dataHolder.categoryAssignmentAppend({'pid':pid,'catid':catid})
        
    
    def characters(self,content):
        self.currentElemContent += content
        
    def endElement(self, name):
        
        if self.inCategory==1:
            if name == 'online-flag' and self.currentElemContent == 'true':
                self.categoryOnlineFlag = 1
            elif name == 'parent' : 
                self.currentCategoryParent = self.currentElemContent
            elif name == 'category':
                if self.currentCategoryAttrs['category-id'] == 'women-travel-shop-lightweight-layers':
                    s = 1 
                self.reg.dataHolder.allCategoryAppend(self.currentCategoryAttrs['category-id'] , self.currentCategoryParent)  #stores only online categories in a list.
                #self.reg.dataHolder.allCategoriesNodesAppend(self.currentCategoryAttrs['category-id'], self.currentCategoryParent)

                self.inCategory=0
                if self.categoryOnlineFlag==  1:
                    self.reg.dataHolder.onlineCategoryAppend(self.currentCategoryAttrs['category-id'], self.currentCategoryParent )  #stores only online categories in a list. 
                    #self.reg.dataHolder.onlineCategoriesNodesAppend(self.currentCategoryAttrs['category-id'], self.currentCategoryParent)
                    self.categoryOnlineFlag=0  #probably dont need this line 
                    self.currentCategoryParent = None
        self.currentElem = ''
    
    def startDocument(self):
        pass
    
    def endDocument(self):
        pass
            
    def getOnlineCategories(self):
        return self.onlineCategories
    
     
        
        
        
        
        
        
        #    <category-assignment category-id="women-t-shirts-and-tops-essential-tees" product-id="422692">
    # <category category-id="trend-report-stripes-for-days">
        # <online-flag>true</online-flag>
    #     <online-from>2020-01-15T14:00:00.000Z</online-from>
    #     <parent>trend-report</parent>
    #     <custom-attributes>
    #         <custom-attribute attribute-id="showInMenu">false</custom-attribute>
    #     </custom-attributes>
    # </category>

    
    
