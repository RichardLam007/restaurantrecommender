'''
Created on Apr 24, 2013

@author: Kathy
'''
import sys, traceback, ast, json

class Extraction:
    '''
    Class that extracts the necessary information from the dataset
    '''
    def __init__(self, userFile, bussFile):
        '''
        Constructor
        '''
        self.users = dict()  #stores the information on the users
        self.businesses = dict()  #stores the information on the restaurants
        self.fileoffset = 0  #used for retrieving the reviews from the dataset
        self.userFilename = userFile  #stores the filename for the file containing the user info
        self.bussFilename = bussFile  #stores the filename for the file containing the business info
    
    
    def extractInfo(self):
        '''
        Extract the necessary information on the users and restaurants
        '''
        f = open('tmpNFvucr', 'r')
    
        #read each line in the file to retrieve the necessary info
        for lcurr in f:        
            line = json.loads(lcurr)  #convert the string into a dictionary object
            
            if line['type'] == "user":
                #add the user to the list if they are not already in it
                if line['user_id'] not in self.users:
                    self.users.update({line['user_id']: dict()})
                    self.users[line['user_id']].update({'name': line['name'], 'reviews': [], 'businesses': []})      
            #if the entry is about a user's review
            if line['type'] == "review":
                #add each restaurant the user has visited to that user's list    
                if line['business_id'] not in self.users[line['user_id']]['businesses']:
                    self.users[line['user_id']]['businesses'].append('business_id')
                if line['review_id'] not in self.users[line['user_id']]['reviews']:
                    self.users[line['user_id']]['reviews'].append('review_id')
            #if the entry is about a business
            elif line['type'] == "business":
                #add every unique restaurant or bar along with some information on them
                if line['business_id'] not in self.businesses and ("Restaurants" in line['categories'] or "Food" in line['categories'] or "Bars" in line['categories']):
                    self.businesses.update({line['business_id']: dict()})
                    self.businesses[line['business_id']].update({'name': line['name'], 'state': line['state'], 'city': line['city'], 'categories': line['categories'] })      
        f.close()

        #Store the dictionaries as json objects
        with open(self.userFilename, 'w') as outfile:
            json.dump(self.users, outfile)
        with open(self.bussFilename, 'w') as outfile:
            json.dump(self.businesses, outfile)      


    def nextReview(self):
        '''
        Obtain the next review entry (a dictionary) on a restaurant/bar from the dataset
        If an entry is not about a restaurant/bar then it is skipped over
        '''  
        reviewFound = False  #flag for whether or not the next review could be found  
        while reviewFound == False:
            f = open('tmpNFvucr', 'r')
            
            #skip to the middle of the file according to the offset and obtain the entry
            f.seek(self.fileoffset)
            tline = f.readline().strip()
            while tline == "":
                tline = f.readline().strip() 
            currLine = json.loads(tline)  #convert the string into a dictionary object
            
            #ignore all the entries about just the users
            while currLine['type'] == "user":
                currLine = ast.literal_eval(f.readline())
            
            #return an empty dictionary if there are no more reviews in the dataset
            if currLine['type'] == "business":
                currLine = {}
                reviewFound = True
                self.fileoffset = 0  #reset the offset into the file back to the beginning
            #otherwise adjust the offset into the file for the next read  
            else:
                #only indicate that a review was found if it is either a restaurant or a bar
                if currLine['business_id'] in self.obtainBussInfo():
                    reviewFound = True
                self.fileoffset = f.tell() - 1
            
            f.close()
        
        return currLine
    
    
    def obtainUserInfo(self):
        '''
        Retrieve the dictionary on the users from the file
        '''        
        userInfo = json.load(open(self.userFilename, 'r'))
        return userInfo
    

    def obtainBussInfo(self):
        '''
        Retrieve the dictionary on the restaurants from the file
        '''
        bussInfo = json.load(open(self.bussFilename, 'r'))
        return bussInfo 
    

    def obtainUserContent(self, userID, category):
        '''
        Obtain a specific data member of the user dictionary
        If category = 'name' then a string containing the user's name will be returned 
        If category = 'reviews' then a list of the review_ids of the reviews the user has made will be returned
        If category = 'businesses' then a list of the business_ids of the restaurants the user has visited will be returned
        '''
        userDict = self.obtainUserInfo()
        return userDict[userID][category]
    

    def obtainBussContent(self, bussID, category):
        '''
        Obtain a specific data member of the restaurant dictionary
        If category = 'name' then a string containing the restaurant's name will be returned
        If category = 'state' then a string containing the state the restaurant is located in will be returned
        If category = 'city' then a string containing the city the restaurant is located in will be returned
        if category = 'categories' then a list containing the categories of the restaurant will be returned
        '''
        bussDict = self.obtainBussInfo()
        return bussDict[bussID][category]
