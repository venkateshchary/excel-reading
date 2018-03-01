#author = "venkatesh"
#Excel file reading
from myLogger import LOG
import datetime
import MongoOperations
import xlrd
import config



class ExcelReading:

    def __init__(self,path,sheetIndex):
        self.filepath = path
        self.sheetindex = sheetIndex

    def cellval(self, cell, datemode):

        if (cell.ctype == xlrd.XL_CELL_DATE):
            try:
                datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
            except Exception as e:
                print("BAD", cell, e)
                return str(cell)
            try:
                if datetuple[:3] == (0, 0, 0):
                    date_time = datetime.time(datetuple[3], datetuple[4], datetuple[5])
                    total_minutes = (date_time.hour / 60 + date_time.minute + date_time.second / 60)
                    return date_time
                return datetime.datetime(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4],datetuple[5])
            except Exception as e:
                print("BAD value 1", datetuple, cell, e)
                return str(cell)
        return cell.value

    def objectformation(self):
        try:
            objList=[]
            book = xlrd.open_workbook(self.filepath)
            sheet = book.sheet_by_index(self.sheetindex)
            sheet_headers = ["".join(str(sheet.cell(0, col_index).value).lower().replace('.',"").split()) for col_index in range(sheet.ncols)]
            for row_index in range(1, sheet.nrows):
                row = sheet.row(row_index)
                values = [self.cellval(c, book.datemode) for c in row]
                obj = dict(zip(sheet_headers, values))
                objList.append(obj)
            #Connecting to mongoOperations
            mongo= MongoOperations.MongoConnection()
            mongo.uploaddata(config.collectionName,objList)
                
        except Exception as error:
            LOG.info("Exception occurred while forming the objects:%s"%error)
            


if __name__ == "__main__":
    
    excel = ExcelReading(config.basePath,0) #excel sheet by index like is sheet1 = index 0 ..etc
    excel.objectformation()


    
