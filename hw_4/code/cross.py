import bayes
import bayesbest
import os

def ten_fold():

	pos_true = 0
	pos_false = 0
	neg_true = 0
	neg_false = 0

	best_pos_true = 0
	best_pos_false = 0
	best_neg_true = 0
	best_neg_false = 0

	bc = bayes.Bayes_Classifier()
	bcc = bayesbest.Bayes_Classifier()
	for i in range(10):
		print "Starting fold: ", i
		testing,training = single_fold(i)
		retrain(bc,training)
		retrain(bcc,training)
		print "\tDone training"
		ct = 1
		for f in testing:

			sTxt = bc.loadFile("movies_reviews/" + f)
			print "\tLoaded: ",ct
			bc_result = bc.classify(sTxt)
			bcc_result = bcc.classify(sTxt)
			print "\tTested: " ,ct
			ct += 1

        	if (f.startswith("movies-5")):
   				if bc_result == "positive":
   					pos_true += 1
   				else:
   					pos_false += 1

   				if bcc_result == "positive":
   					best_pos_true += 1
   				else:
   					best_pos_false += 1

   			elif (f.startswith("movies-1")):
   				if bc_result == "negative":
   					neg_true += 1
   				else:
   					neg_false += 1

   				if bcc_result == "negative":
   					best_neg_true += 1
   				else:
   					best_neg_false += 1
        	
		print "\treg results: %d %d %d %d" % pos_true, pos_false, neg_true, neg_false
		print "\tbest results: %d %d %d %d" % best_pos_true, best_pos_false, best_neg_true, best_neg_false



def single_fold(start_val):
	count = start_val%10 #10 fold validation
	IFileList = []
   	for fFileObj in os.walk("movies_reviews/"):
   		IFileList = fFileObj[2]
   		break
   	training_set = []
   	testing_set = []
   	for f in IFileList:
   		#Training set
   		if(count == 9):
   			#print "count was: ", count, " ; append to testing_set"
   			testing_set.append(f)
   			count = 0
   		else:
   			#print "count was: ", count, " ; append to training_set"
   			training_set.append(f)
   			count+=1
   	return training_set,testing_set


def retrain(bc, training_set):
    #For each file name, parse and determine if pos (5) or neg (1)
    bc.positive = dict()
    bc.negative = dict()

    for f in training_set:
        #Positive review, add words/frequencies to positive dictionary
        if (f.startswith("movies-5")):
        	bc.dictionary = bc.positive
   		
        #Negative review, add words/frequencies to negative dictionary
        elif (f.startswith("movies-1")):
        	bc.dictionary = bc.negative

        else:
        	#print "error: file didn't start with movies-1 or movies-5"
        	continue

        sTxt = bc.loadFile("movies_reviews/" + f)
        token_list = bc.tokenize(sTxt)
        #print "dictionary: ", dictionary

        for word in token_list:
      		#If word exists in dictionary already, increase frequency by 1
      		if word in bc.dictionary:
      			bc.dictionary[word] +=1
      		#Add word to dictionary with frequency of 1 if it did not already exist
      		else:
      			bc.dictionary[word] = 1 