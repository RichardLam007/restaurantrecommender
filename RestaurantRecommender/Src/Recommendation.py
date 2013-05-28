'''
Created on May 24, 2013

@author: Kathy
'''
import heapq
from math import sqrt

class Recommendation:
    '''
    Class that performs the actual recommendation to produce the top-N restaurants
    '''
    def __init__(self, uid, extObj, restManaObj, topNum):
        '''
        Constructor
        '''
        self.userid = uid  #store the userID of the user being recommended
        self.extractor = extObj  #stores the Extraction object to retrieve information
        self.restManager = restManaObj  #stores the RestaurantManager object
        self.rankHeap = []  #the heap used to determine the top-N results
        self.topN = topNum  #store the number of results to obtain (the N in the top-N results)
    
    
    def compareRestaurantRanks(self):
        '''
        Calculates and inserts the rank for each restaurant into the heap
        '''
        attributeDict, reasonDict, categoryList = self.obtainVisitedProperties()  #get the combined properties of the visited restaurants
        allBussDict = self.extractor.obtainBussInfo()  #get the dictionary on all restaurants in the dataset
        #for each of the restaurants in the dataset calculate its rank and attempt to add it into the heap
        for bussid in allBussDict:
            restObj = self.restManager.returnRestaurant(bussid)  #get the restaurant object for this restaurant
            bussAttriDict = restObj.returnAttributes()  #get the attributes of the restaurant
            bussReasonDict = restObj.returnReasons()  #get the reasons for going to the restaurant
            bussCatList = restObj.returnRestaurantData('categories')  #get the restaurant's categories
            restName = restObj.returnRestaurantData('name')  #get the name of the restaurant
            rankVal = 0  #store the ranking value of the restaurant
            numMatches = 0  #counter for the number of matching properties with restaurants the user has visited
            
            #for every matching attribute append attribute value to total
            for attr in bussAttriDict:
                if attr in attributeDict:
                    rankVal = rankVal + bussAttriDict[attr]
                    numMatches = numMatches + 1
            #for every matching reason append reason value to total
            for reason in bussReasonDict:
                if reason in reasonDict:
                    rankVal = rankVal + bussReasonDict[reason]
                    numMatches = numMatches + 1
            #for every matching category append value=1 to total
            for cat in bussCatList:
                if cat in categoryList:
                    rankVal = rankVal + 1
                    numMatches = numMatches + 1
            
            #calculate the average value (total_value/#matches) as the final ranking value 
            if numMatches != 0:
                restRankVal = rankVal / numMatches
            else:
                restRankVal = 0
            
            #if there are fewer than N results in the heap currently then add the restaurant to it
            if len(self.rankHeap) < int(self.topN):
                heapq.heappush(self.rankHeap, (restRankVal, restName))
            #otherwise only keep the set of restaurants with the N highest ranks in the heap
            else:
                heapq.heappushpop(self.rankHeap, (restRankVal, restName))
        

    def obtainVisitedProperties(self):
        '''
        Obtain the properties of the restaurants the user has visited
        Returns a dictionary of the combined attributes of those restaurants
        Also returns a dictionary of the combined reasons for going to those restaurants
        Also returns a list of the combined categories of those restaurants
        '''
        attributeDict = dict()  #stores the combined attributes of the visited restaurants
        reasonDict = dict()  #stores the combined reasons for going to the restaurants
        categoryList = []  #stores the combined categories for the visited restaurants
        userBussList = self.extractor.obtainUserContent(self.userid, "businesses")  #get the dictionary of restaurants the user has visited
        for bussid in userBussList:
            restObj = self.restManager.returnRestaurant(bussid)  #get the restaurant object for this restaurant
            if restObj is None:
                continue

            objAttriDict = restObj.returnAttributes() #get the attributes of the restaurant
            for attri in objAttriDict:
                #if the attribute already exists then add the new value to the overall value of the attribute
                if attri in attributeDict:
                    attributeDict[attri] = self.additionFormula(attributeDict[attri], objAttriDict[attri])
                else:
                    attributeDict[attri] = objAttriDict[attri]
            
            objReasonDict = restObj.returnReasons() #get the reasons for going to the restaurant
            for reason in objReasonDict:
                #if the reason already exists then add the new value to the overall value of the reason
                if reason in reasonDict:
                    reasonDict[reason] = self.additionFormula(reasonDict[reason], objReasonDict[reason])
                else:
                    reasonDict[reason] = objReasonDict[reason]
            
            categoryList = list(set(categoryList + restObj.returnRestaurantData('categories')))  #get the restaurant's categories
        
        return attributeDict, reasonDict, categoryList


    def additionFormula(self, base, additive):
        '''
        return the computed addition of the two given attributes/reasons
        '''
        if base < 1:
            return additive
        return base + additive/(sqrt(abs(base)))

  
    def recommendRestaurants(self):
        '''
        Calculate and return the list of top-N restaurant results
        '''
        self.compareRestaurantRanks()  #fill up the heap with the top-N restaurants and their respective rank values
        topresults = heapq.nlargest(int(self.topN), self.rankHeap)  #get the top-N results sorted in descending order
        return topresults
        