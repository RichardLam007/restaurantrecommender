'''
Created on Apr 24, 2013

@author: EliteCrew
'''
import sys, traceback, ast

class Extractor:
    def __init__(self):
        self.users = dict()
        #self.reviews = dict()
        self.businesses = dict()
    
    def extractInfo(self):
        f = open('tmpNFvucr', 'r')
    
        for lcurr in f:        
            try:
                line = ast.literal_eval(lcurr)
            #some of the entries result in an issue with malformed strings for some reason
            except ValueError:
                continue
    
            #if the entry is about a user's review
            if line['type'] == "review":
                #add the user to the list if they are not already in it
                if line['user_id'] not in self.users:
                    self.users.update({line['user_id']: dict()})
                    self.users[line['user_id']].update({'reviews': [], 'businesses': []})
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
        
        
def main():
    ext = Extractor()
    
    
if __name__ == '__main__':
    try:
        main()
    except:
        print 'Error: ', str(sys.exc_info()[0])
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print 'Description: ', str(exc_value)
        traceback.print_tb(exc_traceback, limit=10, file=sys.stdout)       