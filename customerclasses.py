class CustomerClass(object):
    """Base class for defining the type of customer for which loyalty points will apply"""
    def __init__(self, classType, minMoneyThreshold, maxMoneyThreshold, **kwargs):
        self.classType = classType
        self.minMoneyThreshold = minMoneyThreshold
        self.maxMoneyThreshold = maxMoneyThreshold
    """
    returns a tuple of bool and int, first part is whether this class is applicable or not
    and second is what is the amount for which points are to be calculated for this class type.
    if total money spent including transaction amont and spent previously are within the min and max
    threshold of this class, then the points will be applied on only the applicable money which belong
    in this threshold
    """
    def getApplicableAmount(self, totalMoneySpent, transactionAmount):
        totalSpentSoFar = (totalMoneySpent + transactionAmount)
        amountForPoints = 0
        if ( totalSpentSoFar <= self.minMoneyThreshold):
            return amountForPoints

        if (totalSpentSoFar <= self.maxMoneyThreshold and totalMoneySpent > self.minMoneyThreshold):
            amountForPoints = transactionAmount
        elif (totalSpentSoFar > self.maxMoneyThreshold and totalMoneySpent > self.minMoneyThreshold):
            amountForPoints = (self.maxMoneyThreshold - totalMoneySpent)
        elif (totalSpentSoFar <= self.maxMoneyThreshold and totalMoneySpent <= self.minMoneyThreshold):
            amountForPoints = (totalSpentSoFar - self.minMoneyThreshold)
        elif (totalSpentSoFar > self.maxMoneyThreshold and totalMoneySpent <= self.minMoneyThreshold):
            amountForPoints = (self.maxMoneyThreshold - self.minMoneyThreshold)
        
        return amountForPoints

    """ 
        Function to check applicability of this class and get points for a transaction 
        We check if the current transaction makes this class applicable to that user or not
        which is a function of totalpoints so far, total money spent and current transaction amount
    """
    def getPointsForCustomer(self, totalMoneySpent, totalPointsSoFar, transactionAmount):
        return NotImplementedError("This function is to implemented in derived classes")

    def __str__(self):
        return self.classType

class NormalClass(CustomerClass):
    def __init__(self,classType, minMoneyThreshold, maxMoneyThreshold, joiningBonus = 100, **kwargs):
        super(NormalClass, self).__init__(classType, minMoneyThreshold, maxMoneyThreshold, **kwargs)
        self.joiningBonus = joiningBonus

    def getPointsForCustomer(self, totalMoneySpent, totalPointsSoFar, transactionAmount):       
        amountForPoints = self.getApplicableAmount(totalMoneySpent, transactionAmount)
        transactionPoints = 0
        if amountForPoints > 0:
            transactionPoints = int(0.01*(transactionAmount))
        if totalPointsSoFar == 0:
            transactionPoints += self.joiningBonus
        return transactionPoints


"""
Here assumption is that if the customer spends amount less than the min amount, then
he doesnt get any points for that transaction (eg. )
"""

class SilverClass(CustomerClass):
    def getPointsForCustomer(self, totalMoneySpent, totalPointsSoFar, transactionAmount):
        amountForPoints = self.getApplicableAmount(totalMoneySpent, transactionAmount)
        return int(2*(amountForPoints/100))


class GoldClass(CustomerClass):
    def getPointsForCustomer(self, totalMoneySpent, totalPointsSoFar, transactionAmount):
        amountForPoints = self.getApplicableAmount(totalMoneySpent, transactionAmount)
        return int(25*(amountForPoints/500))
        
        
        