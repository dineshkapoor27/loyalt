#########################################################
README FOR EXECUTING THE LOYALTY PROGRAM CODE
#########################################################

Code Structure:

1. Main.py: The execution for the loyalty program calculation starts from this
file. The usage of this is: [python main.py --datafile <file path>]. The datafile
is optional and by default, the code will look for data.csv in the same folder of main.py. This will process the valid customer transactions for loyalty and print on
the screen.

2. Dataextractors.py: Contains the classes for execution of the code. Most important 
class in this is TransactionProcessor class which reads the data row from the transaction file and processes it. It will parse the data, extract the relevant values and add the transaction points to the customer's transaction history. It also contains instances of the points calculator classes. These classes are applied for all the transactions and if the class is applicable for that transaction, then it will produce a set of points which will be added to the user. 

Other class is the DataExtractor and CsvDataExtractor classes. Former is the base class and latter is an implementation of that class. DataExtractor class enforces the readDataRows function which will provide the iterator for the input of transactions. This can be derived for specific implementations for reading data from other sources as well. Csv implementation has been provided.

3. Datastorage.py: There is a DataTable class for storing data in a tabular format. With this class, user can create a table of any number of column. A primary key index is to be provided in the constructor which will be the location of the primary key in the data row which will be added in it. The primary key will be indexed as dictionary key in the internal implementation. The class provides implementation which can merge the incoming data row with an existing one for the same primary key, if the new data contains different information. It also provides ways to filter, query and print data.

4. customerclasses.py: This class contains the implementation and business logic of the different class types which can be added by deriving from CustomerClass base class. The functions which are expected are to be overriden is getPointsForCustomer for every class which is derived. The class implementations (Normal, Gold, Silver) have specific overriden getPointsForCustomer functions. The instances of these classes are added in the Transaction Processor class for calculating eligibility of a class and total points for the user for every transaction in that class. If a transaction doesnt come in the threshold of that class, then the total points for that class is 0. 

5. tests.py: A generic class based implementation of the unit tests only for illustrative purposes. In this, an instance of the TransactionUnitTests is created and all the functions of this class instance are called one by one. If any of them fails, then we print it out on the screen. The way to run unit test:

python tests.py