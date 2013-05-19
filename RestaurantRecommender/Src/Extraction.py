'''
Created on Apr 24, 2013

@author: Kathy
'''
import sys, traceback, ast, json

class Extractor:
    #Constructor
    def __init__(self):
        self.users = dict()
        #self.reviews = dict()
        self.businesses = dict()
        self.fileoffset = 0
    
    #Extract the necessary information on the users and restaurants
    def extractInfo(self):
        f = open('tmpNFvucr', 'r')
    
        for lcurr in f:        
            try:
                line = ast.literal_eval(lcurr)
            #some of the entries result in an issue with malformed strings for some reason
            except ValueError:
                continue
            
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
                #if line['review_id'] not in self.reviews:
                #    self.reviews.update({line['review_id'] : dict()})
                #    self.reviews[line['review_id']].update({'attributes':[], 'business_id': line['business_id']})
            #if the entry is about a restaurant
            elif line['type'] == "business":
                #add every unique and open business along with some information on them
                if line['business_id'] not in self.businesses and line['open'] == "true":
                    self.businesses.update({line['business_id']: dict()})
                    self.businesses[line['business_id']].update({'name': line['name'], 'state': line['state'], 'city': line['city'], 'categories': ast.literal_eval(line['categories']) })       
        f.close()

        #Store the dictionaries as json objects
        with open('userinfo.json', 'w') as outfile:
            json.dump(self.users, outfile)
        with open('bussinfo.json', 'w') as outfile:
            json.dump(self.businesses, outfile)     

    #Obtain the next review entry from the dataset
    def nextReview(self):
        f = open('tmpNFvucr', 'r')
        
        #skip to the middle of the file according to the offset
        f.seek(self.fileoffset)
        tline = f.readline().strip()
        while tline == "":
            tline = f.readline().strip() 
        
        try:
            currLine = ast.literal_eval(tline)
        except:
            self.fileoffset = 0  #reset the offset into the file back to the beginning
            return {}  #indicate there are no more reviews in the dataset
        
        #ignore all the entries about just the users
        while currLine['type'] == "user":
            currLine = ast.literal_eval(f.readline())
        
        #return an empty dictionary if there are no more reviews in the dataset
        if currLine['type'] == "business":
            currLine = {}
            self.fileoffset = 0  #reset the offset into the file back to the beginning
        #otherwise adjust the offset into the file for the next read  
        else:
            self.fileoffset = f.tell() - 1
        
        f.close()
        return currLine
