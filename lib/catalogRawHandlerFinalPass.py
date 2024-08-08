from .file import File
from lib.catalogOutFile import catalogOutFile

#  catalog file, in or out either.
class catalogRawHandlerFinalPass( ):
    catalogOutFile = None
    catalogInFile = None
    reg = None
    
    def __init__(self, reg, catalogInFile, catalogOutFile): 
        self.reg = reg
        self.catalogOutFile = catalogOutFile
        self.catalogInFile = catalogInFile

    #read entire catalog, parsing raw line by line
    
    def parse(self):
        fh = self.catalogInFile.getFileHandler()
        inProduct=0
        inVariants=0
        inVariantsVariant=0
        targetCurrentProduct=0
        variantIndex = None
        inCategoryAssignment = 0
        targetCurrCategoryAssignmentPID = 0 
        inCustomAttributes = 0
        shippingRegionsFound = 0
        self.isdebugprinting = 0
        for line in fh:
            if '<product product-id=' in line:
                inProduct=1
                currPid = line.split('"')[1]
                if currPid in self.reg.dataHolder.masterCatProducts or currPid in self.reg.dataHolder.variantProducts:
                    targetCurrentProduct=1
                shippingRegionsFound = 0 #reset this flag
            elif '<category-assignment category-id=' in line:
                inCategoryAssignment = 1
                currCategoryAssignmentPID = line.split('"')[3]
                if currCategoryAssignmentPID in self.reg.dataHolder.masterCatProducts  or currCategoryAssignmentPID in self.reg.dataHolder.variantProducts:
                    targetCurrCategoryAssignmentPID = 1

            if inProduct==1:
                if targetCurrentProduct == 1:
                    if  '<online-flag>f' in line:
                        line = line.replace('false','true')
                    elif '<online-flag site-id' in line:
                        line = line.replace('false','true')
                    elif '<searchable-flag>f' in line:
                        line = line.replace('false','true')
                    elif '<available-flag>f' in line:
                        line = line.replace('false','true')
                    elif '<variants>' in line:
                        inVariants = 1
                        variantIndex = 0
                    elif '<custom-attributes>' in line:
                        inCustomAttributes = 1
                    elif inCustomAttributes == 1 and '<custom-attribute ' in line and 'id="shippingRegions">' in line:
                        inShippingregionsCustomAttribute = 1
                        shippingRegionsFound=1
                    elif inShippingregionsCustomAttribute == 1 and '<value>0</value>' in line:
                        pass
                    elif inShippingregionsCustomAttribute == 1 and '<value>1</value>' in line:
                        pass
                    elif inShippingregionsCustomAttribute == 1 and '<value>2</value>' in line:
                        pass
                        
                    elif inVariants == 1 and '<variant product-id=' in line:
                        inVariantsVariant = 1
                        
                    if inVariants == 1:
                        if inVariantsVariant == 1:
                            try:
                                pid = line.split('"')[1]
                                if pid in self.reg.dataHolder.variantProducts:  # only write if its of the limited group of variants we chose
                                    if variantIndex == 0:
                                        defaultline = '                <variant product-id="'+pid+'" default="true"/>\n'
                                        self.writeData(defaultline)
                                    else:
                                        self.writeData(line)
                                    variantIndex += 1
                                inVariantsVariant = 0
                            except Exception as e:
                                print(e)
                        else: #variants or /variants 
                            self.writeData(line)
                    else:
                         self.writeData(line)
                    if '</variants>' in line:
                        inVariants=0
                        variantIndex = None
                    elif '</custom-attribute>' in line:
                        inShippingregionsCustomAttribute = 0
                    elif '</custom-attributes>' in line:
                        inCustomAttributes = 0
            elif inCategoryAssignment == 1:
                if targetCurrCategoryAssignmentPID == 1:
                    self.writeData(line)
            else: # not in product so print it all. 
                self.writeData(line)
                
            if '</product>' in line:
                inProduct = 0
                targetCurrentProduct = 0
                shippingRegionsFound = 0
            elif '</category-assignment' in line  or  ( '<category-assignment category-id=' in line and '"/>' in line):
                inCategoryAssignment = 0 
                targetCurrCategoryAssignmentPID = 0
        self.catalogOutFile.flush()
        self.catalogOutFile.close()
        
    def writeData(self, line):
        stripped = line.strip()
        if stripped != '':
            self.catalogOutFile.writeString(line)
        if self.isdebugprinting == 1:
            print(line)