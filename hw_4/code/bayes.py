# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re
import os.path

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

      print "reg bayes"
      #for calculating prior probabilities of positive & negative reviews
      self.num_positive_reviews = 0
      self.num_negative_reviews = 0

      # If either dictionary does not exist, create new ones and train
      if(not os.path.isfile("positive.pickle")) or (not os.path.isfile("negative.pickle")):
         self.positive = dict()
         self.negative = dict()
         self.train()
         self.calc_num_reviews()
         pickle.dump(self.positive, open("positive.pickle",'w'))
         pickle.dump(self.negative, open("negative.pickle",'w'))

      #IF both exist, load the pickled dictionaries
      else:
         self.positive = pickle.load(open("positive.pickle"))
         self.negative = pickle.load(open("negative.pickle"))
         self.calc_num_reviews()

   def train(self):   
      	"""Trains the Naive Bayes Sentiment Classifier."""
   	#Get list of all filenames in the review folder
   	IFileList = []
   	for fFileObj in os.walk("movies_reviews/"):
   		IFileList = fFileObj[2]
   		break
   	
      #For each file name, parse and determine if pos (5) or neg (1)
   	for f in IFileList:

         #Positive review, add words/frequencies to positive dictionary
         if (f.startswith("movies-5")):
            dictionary = self.positive
   		
         #Negative review, add words/frequencies to negative dictionary
         elif (f.startswith("movies-1")):
            dictionary = self.negative

         else:
            #print "error: file didn't start with movies-1 or movies-5"
            continue

         sTxt = self.loadFile("movies_reviews/" + f)
         token_list = self.tokenize(sTxt)
         #print "dictionary: ", dictionary

         for word in token_list:
      		#If word exists in dictionary already, increase frequency by 1
      		if word in dictionary:
      			dictionary[word] +=1
      		#Add word to dictionary with frequency of 1 if it did not already exist
      		else:
      			dictionary[word] = 1 

   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """

      #get tokens
      tokens = self.tokenize(sText)

      #positive
      den = (self.num_positive_reviews+self.num_negative_reviews)
      prior_prob = float(self.num_positive_reviews)/den
      log_sum = calc_log_sum(tokens, self.positive)
      prob_pos_given_features = log_sum + math.log(prior_prob)

      prior_prob = float(self.num_negative_reviews)/den

      log_sum = calc_log_sum(tokens, self.negative)
      prob_neg_given_features = log_sum + math.log(prior_prob)

      if prob_pos_given_features > prob_neg_given_features:
         return "positive"

      elif prob_pos_given_features < prob_neg_given_features:
         return "negative"

      else:
         return "neutral"

   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens

   def calc_num_reviews(self):
      IFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         IFileList = fFileObj[2]
         break
      
      #For each file name, parse and determine if pos (5) or neg (1)
      for f in IFileList:
         if (f.startswith("movies-5")):
            self.num_positive_reviews += 1
         
         #Negative review, add words/frequencies to negative dictionary
         elif (f.startswith("movies-1")):
            self.num_negative_reviews += 1

         else:
            #print "error: file didn't start with movies-1 or movies-5"
            continue

def calc_log_sum(tokens, the_dict):

      num_features = 0
      for key in the_dict:
         num_features += the_dict[key]

      log_sum = 0
      for token in tokens:
         if(token in the_dict):
            log_sum += math.log(float(the_dict[token]+1) /num_features) #black-swan effect
         else:
            log_sum += math.log(1/float(num_features))

      return log_sum


	
