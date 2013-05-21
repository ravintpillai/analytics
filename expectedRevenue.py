import getSiteDicts as sd
import sys

class siteData(object):
    def __init__(self, site):
        self.site = site
        self.data = sd.Data[site]
        
    def getData(self):
        return self.data
    
    def getSite(self):
        return self.site
    
    def expectedPercentages(self, hour):
        previousRevTotal = 0
        previousRevCumulativeDict = {}
        rev = 0
        ## Create a dictionary of previous hours cumulative revenue
        for items in self.getData()[1]:
            rev += self.getData()[1][items]
            previousRevCumulativeDict[items] = rev
            
        totalRev = rev

        try:
            assert previousRevCumulativeDict[23] == totalRev
        except:
            print "Total revenue != Total revenue. Panic."
        
        try:
            expectedPercentageValue = previousRevCumulativeDict[hour]/totalRev
            return expectedPercentageValue
        except ZeroDivisionError:
            print "Sum of total revenue = 0"
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def cumulativeRevenue(self,hour):
        rev = 0
        for hours in range(hour+1):
            try:
                rev += self.getData()[0][hours]
            except(KeyError):
                pass
        return rev
    
    def duckworthPredictor(self,hour):
        EP = self.expectedPercentages(hour)
        print "Expected percentage : ",EP
        print self.getData()[0][hour]
        print self.getData()[0]
        try:
            return self.cumulativeRevenue(hour)/EP
        except ZeroDivisionError:
            print "Sum of total revenue = 0"
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


        
