"""
This is the base class for data extraction from the data sources. Sources can be
csv, text file or even a remote network file location. Specific data extraction
methods are to be overriden for specific data reading
"""
import os
import csv
from datastorage import DataTable
from customerclasses import NormalClass, SilverClass, GoldClass

class DataExtractor(object):
    def __init__(self, dataSourceLocation, **kwargs):
        self.dataSourceLocation = dataSourceLocation

    def readDataRows(self):
        """ method to be overriden for specific implementation, to provide iterator for data source  """
        raise NotImplementedError("This function is to be implemented")


"""
Specific implementation to read data rows from a csv file. 

"""
class CsvDataExtractor(DataExtractor):
    def __init__(self, csvFileLocation):
        if os.path.isfile(csvFileLocation):
            self.headers = None
            super(CsvDataExtractor, self).__init__(csvFileLocation)
        else:
            raise Exception("The CSV File doesnt exist on this location: %s"%(csvFileLocation))

    '''
    It yields a data Iterator, and it is assumed that the first row is always the header
    '''
    def readDataRows(self):
        with open(self.dataSourceLocation, "rb") as csvFile:
            reader = csv.reader(csvFile)       
            for row in reader:
                yield row


# Main class for processing the data input from the data source

class TransactionProcessor(object):
    """Class to validate and process data row for loyalty points """
    UserKey = 2
    AmountKey = 3
    TransactionDateTimeKey = 4
    TransactionIdKey = 5

    def __init__(self, **kwargs):
        super(TransactionProcessor, self).__init__()
        self.getNewCustomerTable()
        self.getNewTransactionTable()
        self.getPointCalculatorAndClassList()
        self.transactionDataSchemaLength = 0
        

    # customer table for keeping the customer data related to overall spend and total points
    def getNewCustomerTable(self):
        defaultTableName = 'Customer'
        defaultColumnsList = ['Name', 'Email Address', 'Loyalty Card No', 'Current Class', 'Total Amount', 'Total Points']
        self.customerTable = DataTable(defaultTableName, defaultColumnsList, 2)
    
    def setSchemaLength(self, schemaLength):
        self.transactionDataSchemaLength = schemaLength

    #generates a transaction table for keeping mapping of user transactions and points earned
    def getNewTransactionTable(self):
        userTransactionsTableName = 'Transactions'
        transactionColsList = [ 'Customer', 'Date Time', 'Transaction Id', 'Transaction Amount', 'Points Earned']
        self.transactionTable = DataTable(userTransactionsTableName, transactionColsList, 2)

    # these values can be changed/passed through the constructor, added here for simplicity
    def getPointCalculatorAndClassList(self):
        normal = NormalClass('Normal', 0, 25000)
        silver = SilverClass('Silver', 25000, 50000)
        gold = GoldClass('Gold', 50000, 100000000) # upto 1 crore spent upper limit
        self.pointCalculatorList = [normal, silver, gold] # more types of points accrual and classes can be created and appended to this list


    # Applies the points calculation classes and generates the total points, new class type
    # and total amount spent by the user post this transaction
    def processTransactionAmountForUser(self, transaction, totalAmount):
        newClassType = None
        totalpoints = 0
        for classType in self.pointCalculatorList:
            pointsSoFar = classType.getPointsForCustomer(totalAmount, totalpoints, transaction)
            totalpoints += pointsSoFar
            if pointsSoFar > 0:
                newClassType = classType
        totalAmount += transaction
        return (newClassType, totalAmount, totalpoints)

    '''
     Function which processes every data row from the data source and updates relevant
     data tables of the users and transactions
    '''
    def processDataRowForUser(self, dataRow):
        if not dataRow or len(dataRow) < self.transactionDataSchemaLength:
            return False

        # if loyalty card no. exists in the db
        if self.customerTable.checkIfExists(dataRow[self.UserKey]):
            existingUserKey = dataRow[self.UserKey]
            existingUserRow = self.customerTable.getDataRow(existingUserKey)
            totalAmountSpentSoFar = self.customerTable.getColumnValue(existingUserKey, 'Total Amount')
            totalPointsSoFar = self.customerTable.getColumnValue(existingUserKey, 'Total Points')
            transactionAmount = int(dataRow[self.AmountKey])
            (newClassType, totalAmount, transactionPoints) = self.processTransactionAmountForUser(transactionAmount, totalAmountSpentSoFar)
            
            customerDataRow = dataRow[:self.AmountKey] + [newClassType, totalAmount, (totalPointsSoFar + transactionPoints)]
            self.customerTable.createOrUpdate(customerDataRow)
            
            transactionRow = [existingUserKey, dataRow[self.TransactionDateTimeKey], dataRow[self.TransactionIdKey], dataRow[self.AmountKey], transactionPoints] 
            self.transactionTable.createOrUpdate(transactionRow)

        # if the loyalty card number doesnt exist in the db, then make an entry
        elif dataRow[self.UserKey]:
            newUserKey = dataRow[self.UserKey]
            totalAmountSpentSoFar = 0
            totalPointsSoFar = 0
            transactionAmount = int(dataRow[self.AmountKey])
            (newClassType, totalAmount, transactionPoints) = self.processTransactionAmountForUser(transactionAmount, totalAmountSpentSoFar)
            customerDataRow = dataRow[:self.AmountKey] + [newClassType, totalAmount, (totalPointsSoFar + transactionPoints)]
            self.customerTable.createOrUpdate(customerDataRow)
            
            transactionRow = [newUserKey, dataRow[self.TransactionDateTimeKey], dataRow[self.TransactionIdKey], dataRow[self.AmountKey], transactionPoints] 
            self.transactionTable.createOrUpdate(transactionRow)

        return True

    # This function produces the expected output to the console
    def printFormattedData(self):
        transactionColumns = ['Date Time', 'Transaction Id', 'Transaction Amount', 'Points Earned']
        for customerKey in self.customerTable.getAllPrimaryKeys():
            self.customerTable.printRows([customerKey])
            self.transactionTable.printFilteredRows( self.transactionTable.getRowsByColumn('Customer', [customerKey]), 'Transactions', transactionColumns)
