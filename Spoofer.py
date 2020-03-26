from numpy import ndarray, zeros
import math
import random
# Function used to create initial spoof vector
def createSpoofVector( numFeature : int) -> ndarray:
	testVector = zeros(numFeature)
	for i in range(numFeature):
		testVector = random.random()*26 # get random number from [0 - 26) to represent test data
	return n

# ** final product will be in KeyStroke authenticator over here while I fix up the program **
def fitnessFunction(meanVector : ndarray, testVector : ndarray) -> int:
    if len(meanVector) != len(testVector):
        print("ERROR mean vector and test vector are not the same size")
        print("mean vector:" + (str)(meanVector))
        print("test vector:" + (str)(testVector))
        return -1
    dist = 0
    for i in range(meanVector):
        d = meanVector[i] - testVector[i]
        dist += pow(d, 2) # square the distance and add it
    return dist

class KeyStroke
	def __init__(self, keyStroke : ndarray):
		self.keyStroke = keyStroke
		self.fitness = -1

	def getKeyStroke(self):
		return self.keyStroke

	def setFitness(self, fitness: float):
		self.fitness = fitness

	def getFitness(self):
		if self.fitness == -1:
			raise Exception("ERROR: tried to get fitness without first setting it first")
		return self.fitness

class KeystrokeSpoofer:
	 # ** get user threshold and function used to authenticate from identifier program **
    def __init__(self, numFeature : int, threshold : int,  population : int):
    	self.numFeature = numFeature
    	self.threshold = threshold
    	self.population = population

    def createInitialPopulation(self) -> list :
    	possibleKeyStroke = []
    	for i in range(self.population): # randomly create possible vector in the given space
    		keyStroke = KeyStroke(createSpoofVector())
    		# **** fitness function will come from identifier program *****
    		keyStroke.setFitness(fitnessFunction(keyStroke.getKeyStroke(), testVector))
    		possibleKeyStroke.append(keyStroke)
    	# possibleKeyStroke.sort(key=lambda ndarray : fitnessFunction(meanVector, testVector))
    	possibleKeyStroke.sort(key=lambda KeyStroke : KeyStroke.getFitness())
    	return possibleKeyStroke

    def getMean(self, possibleKeyStroke : list) -> float:
    	mean = 0
    	for p in possibleKeyStroke:
    		mean += p.getFitness()
    	mean /= self.population
    	return mean

    def getStandardDeviation(self, mean : float):
    	variance = 0
    	for p in possibleKeyStroke:
            variance += pow(p.getFitness()-mean,2)           
        variance /= self.population
        return math.sqrt(variance)

    def getParents(self, possibleKeyStroke : list):
    	mean = self.getMean(possibleKeyStroke)
    	sd = self.getStandardDeviation(mean)
    	parents = []
    	for p in possibleKeyStroke: # a parents will be selected more depending on how close they are to the target vector
    		f = p.getFitness()
    		timesSelected = -round((f - mean) / standardDeviation) # basically use z-score to calculate times selected
    		for i in range(timesSelected):
    			parents.add(p)
    	while(len(parent)>self.population):
    		parents.pop(-1)
    	while(len(parents)<self.population)
    		parents.add(parents[])
    	random.shuffle(parents)
    	return parents

    def createSpoof(self):
    	# ** will use the authenticator program to test vector ** for now just use make shift function
    	 #  ** in actual project this will be the mean vector in the authentication program. **
    	testVector = createSpoofVector(self.numFeature) 
    	#  GA function 
    	# 1. Create initial population
    	possibleKeyStroke = self.createInitialPopulation()
    	minScore = possibleKeyStroke[0] # once sorted we can easily get the most fit function
    	while minScore > threshold: # stop condition : when best guess passes threshold
    		# Selection of the best-fit individuals for next generation
    		parents = self.getParents(possibleKeyStroke, mean, sd)
    		# Generate new child by crossover and mutation operations
    		children = self.getChildren(parents) # creates children using parents 
    		# Evaluate new individuals by fitness function according to (4);

    		# Replace the least-fit population with new individuals
    		while 
    		minScore = possibleKeyStroke[0] # once sorted we can easily get the most fit function

    	

# ** will remove from final product and move to main program
if __name__ == '__main__':

       