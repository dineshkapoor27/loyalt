"""
Unit tests file for testing out various classes and their functions.
More tests can be added, but this is added for illustrative purposes

"""

from dataextractors import TransactionProcessor


def executeUnitTests(unitTestObj):
    unitTests = [getattr(unitTestObj, testFunc) for testFunc in dir(unitTestObj) if callable(getattr(unitTestObj, testFunc))]
    if all(map(lambda func: func(), unitTests)):
        print "Unit Tests Passed For %s"%(unitTestObj)
    else:
        print "****Unit Tests Passed For %s****"%(unitTestObj)


class TransactionUnitTests:
    def checkForEmptyTransactionRow(self):
        transaction = []
        processor = TransactionProcessor()
        return (processor.processDataRowForUser(transaction) == False)

    def checkForValidRow(self):
        transaction = ["Anant","anant@mettl.com","11002","7281","24-06-2012 19:18",2938381]
        processor = TransactionProcessor()
        return (processor.processDataRowForUser(transaction) == True)

    def checkForPointsProcessing(self):
        # key = total points, value -> [transaction amount spent, total amount spent so far]
        validTransactionPointsValues = { 150: [5000, 0], 199: [4900, 5000] }
        processor = TransactionProcessor()
        passed = True
        for points, moneySpentVals in validTransactionPointsValues.items():
            passed = passed and (processor.processTransactionAmountForUser(moneySpentVals[0], moneySpentVals[1]) == points)
        return passed

    def __str__(self):
        return 'Transaction Processor'

if __name__ == '__main__':
    transactionTests = TransactionUnitTests()
    executeUnitTests(transactionTests)
        
        