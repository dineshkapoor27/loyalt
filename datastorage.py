"""
Base class for data storage abstraction. Provides basic functionalities for CRUD
of data objects. Specific storage tables need to inherit this class.

"""
import sys
class DataTable(object):
    def __init__(self, tableName, columnsList, primaryKey, **kwargs):
        if (columnsList and (primaryKey < len(columnsList))):
            self.columnsList = columnsList
            self.primaryKey = columnsList[primaryKey]
            self.dataRows = {}
            self.primaryKeyIndex = primaryKey
            self.tableName = tableName
        else:
            raise Exception("Invalid Table columns or Primary Key")

    def _validateDataRow(self, dataRow):
        return (type(dataRow) == list and len(dataRow) == len(self.columnsList) and dataRow[self.primaryKeyIndex])

    def _merge(self, dataRow, primaryKey):
        if not self.dataRows.has_key(primaryKey):
            return dataRow
        existingRow = self.dataRows[primaryKey]
        mergedRow = []
        for index, colValue in enumerate(existingRow):
            if dataRow[index] and dataRow[index] != existingRow[index]:
                mergedRow.append(dataRow[index])
            else:
                mergedRow.append(existingRow[index])
        return mergedRow

    def checkIfExists(self, key):
        return key in self.dataRows.keys()

    def createOrUpdate(self, dataRow):
        if self._validateDataRow(dataRow):
            primaryKeyValue = dataRow[self.primaryKeyIndex]
            self.dataRows[primaryKeyValue] = self._merge(dataRow, primaryKeyValue)

    def getDataRow(self, primaryKeyValue):
        if self.dataRows.has_key(primaryKeyValue):
            return self.dataRows[primaryKeyValue]
        return None

    def deleteDataRow(self, primaryKeyValue):
        if self.dataRows.pop(primaryKeyValue, None):
            return True
        else:
            raise Exception("Invalid Primary Key Value in Delete")

    def printRows(self, primaryKeyList = []):
        dataRowsToBePrinted = []
        if not primaryKeyList:
            dataRowsToBePrinted = self.dataRows.values()
        else:
            dataRowsToBePrinted = map(lambda key: self.dataRows[key] if self.dataRows.has_key(key) else None, primaryKeyList)
        for row in dataRowsToBePrinted:
            for index, column in enumerate(self.columnsList):
                print "%s : %s \n"% (column, row[index])


    def getRowsByColumn(self, columnName, columnValuesList):
        totalRows = []
        if columnName not in self.columnsList:
            return totalRows

        index = self.columnsList.index(columnName)
        for row in self.dataRows.values():
            if row[index] and row[index] in columnValuesList:
                totalRows.append(row)
        return totalRows

    def getColumnValue(self, primaryKey, columnName):
        if self.checkIfExists(primaryKey) and columnName in self.columnsList:
            index = self.columnsList.index(columnName)
            return self.dataRows[primaryKey][index]

    def setColumnValue(self, primaryKey, columnName, colValue):
        if self.checkIfExists(primaryKey) and columnName in self.columnsList:
            index = self.columnsList.index(columnName)
            self.dataRows[primaryKey][index] = colValue

    def getAllPrimaryKeys(self):
        return self.dataRows.keys()

    def printFilteredRows(self, dataRows, dataLabel, selectedCols = None):
        selectedIndexes = map(lambda val: self.columnsList.index(val), selectedCols)
        print "%s: " %(dataLabel)
        for row in dataRows:
            for index, column in enumerate(row):
                if index in selectedIndexes:
                    sys.stdout.write("%s "%(column))
                    sys.stdout.flush()
            print "\n"
