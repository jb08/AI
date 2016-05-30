# Name: Megan Sinclair, David Williams, Jason Brown
# Date: 5/23/16
# All group members were present and contributing during all work on this project
#
# Note that there is a retrain function in this script. This function mirrors the training
#  that is present in our bayes.py and bayesbest.py files. Mirroring it here was simply
#  done to make our cross-validation easier, but bayesbest.py is still intended to be used
#  by itself.

import bayes
import bayesbest
import os, time

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
		training,testing = single_fold(i)
		retrain(bc,training, False)
		retrain(bcc,training, True)
		#print "\tDone training"
		#print len(testing) 
		#print len(training)
		#time.sleep(3)
		ct = 1
		for f in testing:

			sTxt = bc.loadFile("movies_reviews/" + f)
			bc_result = bc.classify(sTxt)
			bcc_result = bcc.classify(sTxt)
			#print "\tTested: " ,ct
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
   		print "fold: ", i
   		print "\treg results: %d %d %d %d" % (pos_true, pos_false, neg_true, neg_false)
   		print "\tbest results: %d %d %d %d" % (best_pos_true, best_pos_false, best_neg_true, best_neg_false)

	#precision
	precision_positive = pos_true / float(pos_true + pos_false)
	precision_negative = neg_true / float(neg_true + neg_false)

	best_precision_positive = best_pos_true / float(best_pos_true + best_pos_false)
	best_precision_negative = best_neg_true / float(best_neg_true + best_neg_false)

	#recall
	recall_positive = pos_true / float(pos_true + neg_false)
	recall_negative = neg_true / float(neg_true + pos_false)

	best_recall_positive = best_pos_true / float(best_pos_true + best_neg_false)
	best_recall_negative = best_neg_true / float(best_neg_true + best_pos_false)

	#f-measure
	f_measure_positive = (2 * precision_positive * recall_positive) / float(precision_positive + recall_positive)
	f_measure_negative = (2 * precision_negative * recall_negative) / float(precision_negative + recall_negative)

	best_f_measure_positive = (2 * best_precision_positive * best_recall_positive) / float(best_precision_positive + best_recall_positive)
	best_f_measure_negative = (2 * best_precision_negative * best_recall_negative) / float(best_precision_negative + best_recall_negative)

	print "naive bayes classifier:"
	print "   precision_positive: %.3f" % precision_positive
	print "   precision_negative: %.3f"% precision_negative
	print "   recall_positive: %.3f" %recall_positive
	print "   recall_negative: %.3f" %recall_negative
	print "   f_measure_positive: %.3f" %f_measure_positive
	print "   f_measure_negative: %.3f" %f_measure_negative
	print " "

	print "naive bayes classifier (improved):"
	print "   precision_positive: %.3f" %best_precision_positive
	print "   precision_negative: %.3f" %best_precision_negative
	print "   recall_positive: %.3f" %best_recall_positive
	print "   recall_negative: %.3f" %best_recall_negative
	print "   f_measure_positive: %.3f" %best_f_measure_positive
	print "   f_measure_negative: %.3f" %best_f_measure_negative

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


def retrain(bc, training_set, is_best):
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
      		
      		if (is_best):
	        	word = word.lower()

      		#If word exists in dictionary already, increase frequency by 1
      		if word in bc.dictionary:
      			bc.dictionary[word] +=1
      		#Add word to dictionary with frequency of 1 if it did not already exist
      		else:
      			bc.dictionary[word] = 1