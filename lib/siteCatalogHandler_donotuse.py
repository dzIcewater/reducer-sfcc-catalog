import xml.sax

#  catalog file, in or out either. 
class siteCatalogHandler(xml.sax.ContentHandler):
    filters=None
    reg = None
    inCategory = 0
    inCategoryAssignment = 0
    categories = {}

    def __init__(self, catalogInfile, reg):
        self.catalogInfile = catalogInfile  
        self.reg = reg

    def startElement(self, name, attrs):
        self.currentElem = name
        if self.currentElem == 'category':
            self.inCategory = 1
            self.onlineflag = 'n/a'
            self.currentCategory = attrs['category-id']
            self.currentAttrs = attrs
        elif self.currentElem == 'category-assignment':
            self.inCategoryAssignment = 1

    def characters(self,content):
        self.content = content

    def endElement(self, name):
        #print('elem was: ' + self.currentElem)
        if self.inCategory == 1:  #in product chunk, so check filter
            pass
        if self.currentElem == 'category':
            self.inCategory = 0
            #now at end of a category, we can apply filter.
            if( self.doesPassFilter()):
                self.appendToCategories(self.currentCategory)

        elif self.currentElem == 'category-assignment':
            self.inCategoryAssignment = 0
            self.appendCategoryAssignment()
        elif self.currentElem == 'online-flag':
            self.onlineflag = self.content             
        
        self.currentElem = ''
    
    # inspect maybe:       currentElem   content   currentAttrs    onlineflag
    def doesPassFilter(self):
        if self.onlineflag == 'true':
            return True
        return False
    
    def appendFilteredProduct(self, productStr):
        pass
    
    def getFilteredProducts(self):
        return self.filteredProducts
        
    def appendToCategories(self, categoryid):
        if categoryid not in self.categories:
            self.categories[categoryid] = []
    
    def appendCategoryAssignment(self):
        catid = self.currentAttrs['category-id']
        pid = self.currentAttrs['product-id']
        if catid in self.categories:
            self.categories.append(pid)
        else:
            raise Exception('appendtocaterror!')
        
        
        #    <category-assignment category-id="Hawaii" product-id="410764"/>
