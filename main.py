'''
The main program starts execution of the loyalty program for points calculation.
The classes used here are 

'''
import argparse, sys
from dataextractors import CsvDataExtractor, TransactionProcessor

def main():
    parser = argparse.ArgumentParser(description='Process transactions for loyalty points.')
    parser.add_argument('--datafile', nargs='+', default="data.csv", type=str)
    args = parser.parse_args()
    
    # defaults to data.csv in the same folder
    transactionFileLocation = args.datafile
    dataextractor = CsvDataExtractor(transactionFileLocation)
    dataHeadersFound = False

    # This is the main executor class object, which parses the data row by row
    # and updates the data tables for users. Also, prints it later
    processor = TransactionProcessor()

    # Iterate over the rows for processing the transactions, first row is assumed
    # to have headers
    for dataRow in dataextractor.readDataRows():
        if not dataRow:
            continue
        if not dataHeadersFound:
            dataHeadersFound = True
            processor.setSchemaLength(len(dataRow))
        else:
            processor.processDataRowForUser(dataRow)

    # print formatted data from the in-memory data tables
    processor.printFormattedData()

if __name__ == '__main__':
    main()