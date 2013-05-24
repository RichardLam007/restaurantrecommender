'''
Created on May 24, 2013

@author: Kathy
'''
import heapq

class Recommendation:
    '''
    Class that performs the actual recommendation to produce the top-N restaurants
    '''
    def __init__(self, extObj, restManaObj, topNum):
        '''
        Constructor
        '''
        self.extractor = extObj  #stores the Extraction object to retrieve information
        self.restManager = restManaObj  #stores the RestaurantManager object
        self.rankHeap = []  #the heap used to determine the top-N results
        self.topN = topNum  #store the number of results to obtain (the N in the top-N results)
    
    def compareRestaurantRanks(self):
        '''
        Insert the rank for each restaurant into the heap
        '''
        restVal = 0
        restName = ""
        restSetDict = self.restManager.obtainAllSets()  #obtain all the restaurant sets
        for restSet in restSetDict:
            restDict = restSetDict[restSet].returnRestaurants()  #obtain the dictionary of restaurants for this set
            for restid in restDict:
                restName = restDict[restid].returnRestaurantData("name")  #Obtain the restaurant's name
                restVal = restDict[restid].returnRank()  #obtain the restaurant's rank
        
                #if there are fewer than N results in the heap currently then add the restaurant to it
                if len(self.rankHeap) < int(self.topN):
                    heapq.heappush(self.rankHeap, (restName, restVal))
                #otherwise only keep the set of restaurants with the N highest ranks in the heap
                else:
                    heapq.heappushpop(self.rankHeap, (restName, restVal))
            
            
    def recommendRestaurants(self):
        '''
        Return the top-N restaurant results
        '''
        self.compareRestaurantRanks()  #fill up the heap with the top-N restaurants and their respective rank values
        topresults = heapq.nlargest(int(self.topN), self.rankHeap)  #get the top-N results sorted in descending order
        return topresults
        