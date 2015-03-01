from z3 import Int

class Table:
    TableRows = 3
    
    def __init__(self, Name, IsADBTable, IsNotCopy = True):
        self.Name = Name
        self.ColumnsByName = {}
        self.ColumsByIndex = {}
        self.Rows = []
        self.PK = []
        self.IsADBTable = IsADBTable
        
        if IsNotCopy:
            if self.IsADBTable:
                DetailsFile = './Resources/'+Name+'Details.txt'
                Details = open(DetailsFile,'r')
                
                self.NumberOfColumns = int(Details.readline())
                for index in range(self.NumberOfColumns):
                    Line = Details.readline()
                    Col = Line.split()
                    Type = Col[0]
                    Name = Col[1]
                    if not (self.ColumnsByName.__contains__(Name)):
                        self.ColumnsByName[Name] = [Type, index]
                    if not (self.ColumsByIndex.__contains__(index)):
                        self.ColumsByIndex[index] = [Type, Name]
                
                Line = Details.readline()
                while (Line != ''):
                    Parts = Line.split()
                    if (Parts[0] == 'PK'):
                        for i in range(len(Parts) - 1):
                            self.PK.append((self.ColumnsByName[Parts[i+1]])[1])
                    
                    elif (Parts[0] == 'FK'):
                        pass
                    
                    Line = Details.readline()
                
                for i in range(self.TableRows):
                        self.addRow()
                
            else:
                pass
            
        else:
            # It is a copy. We will set the details in copy function
            pass    
                
    def getRows(self):
        return self.Rows
        
    def getColumnIndexFromName(self, Name):
        return (self.ColumnsByName[Name])[1]
    
    def getZ3ObjectForTableElement(self,ColIndex, RowNum):
        return self.Rows[RowNum][ColIndex]
    
    def getColumnNameList(self):
        List = []
        for index in self.ColumsByIndex:
            List.append(self.ColumsByIndex[index][1])
        return List
             
    def getColumnTypeList(self):
        List = []
        for index in self.ColumsByIndex:
            List.append(self.ColumsByIndex[index][0])
        return List
              
    def getColumnTypeFromIndex(self, Index):
        return (self.ColumsByIndex[Index])[0]
        
    def getNumberOfRows(self):
        return len(self.Rows)
    
    def getPKColumns(self):
        return self.PK
    
    def addRow(self):
        RowIndex = self.getNumberOfRows()+1
        row = []
        for ColIndex in range(self.ColumsByIndex.__len__()):
            V = self.ColumsByIndex[ColIndex]
            Type = V[0]
            Name = V[1]+ RowIndex.__str__() + ColIndex.__str__()
            row.append(self.getZ3Object(Type, Name))
        
        self.Rows.append(row)
                
    def getZ3Object(self, Type,Name):
        if (Type == 'Int'):
            return Int(Name)
            
        elif (Type == 'String'):
            pass
        
        elif (Type == 'Date'):
            pass
        
    def Copy(self):
        # Makes a Partly Shallow Partly Deep Copy of the Table
        T = Table(self.Name, self.IsADBTable, False)
        T.ColumnsByName = self.ColumnsByName
        T.ColumsByIndex = self.ColumsByIndex
        T.PK = self.PK
        
        for eachrow in self.Rows:
            row = []
            for eachElement in eachrow:
                row.append(eachElement)
            T.Rows.append(row)
        
        return T