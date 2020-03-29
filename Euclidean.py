# Euclidean
# the evaluate method uses the mean vector to compare

from numpy import ndarray, zeros
from KeystrokeAuthenticator import KeystrokeAuthenticator

class Euclidean(KeystrokeAuthenticator):
	def __init__(self):
		super().__init__() 
		self.meanVector =[]
	    
	''' 
	Function takes every keystroke in the training set creates a vector with the average score of all
	'''
	def trainModel(self, userTestVectors : list) -> list: 
	    if len(self.meanVector)!= 0:
	    	raise Exception("ERROR: Tying to retrain Euclidean model")
	    numFeature = len(userTestVectors[0])
	    sumVector = zeros(numFeature)
	    for userVector in userTestVectors: 
	    	for i in range(numFeature):
	    		sumVector[i] += userVector[i]
	    for i in range(numFeature):
	    	self.meanVector.append(sumVector[i]/len(userTestVectors))
	    # print("sum" ,sumVector)
	    # print("mean" ,self.meanVector)
	     

	def evaluate(self, testVector : ndarray) -> float:
	    if len(self.meanVector) != len(testVector):
	        print("mean vector:" + (str)(self.meanVector))
	        print("test vector:" + (str)(testVector))
	        raise Exception("ERROR: mean vector and test vector are not the same size")
	    dist = 0
	    for i in range(len(self.meanVector)):
	        d = self.meanVector[i] - testVector[i]
	        dist += pow(d, 2) # square the distance and add it
	    return dist.item()
