from numpy import ndarray, zeros, mean, std
import math
import random
from KeystrokeAuthenticator import KeystrokeAuthenticator
# Function used to create initial spoof vector
def createSpoofVector( numFeature : int) -> ndarray:
    testVector = zeros(numFeature)
    for i in range(numFeature):
        testVector[i] = random.random()*26 # get random number from [0 - 26) to represent test data
    return testVector

# ** final product will be in Keystroke authenticator over here while I fix up the program **
def fitnessFunction(meanVector : ndarray, testVector : ndarray) -> float:
    if len(meanVector) != len(testVector):
        print("ERROR mean vector and test vector are not the same size")
        print("mean vector:" + (str)(meanVector))
        print("test vector:" + (str)(testVector))
        return -1
    dist = 0
    for i in range(len(meanVector)):
        d = meanVector[i] - testVector[i]
        dist += pow(d, 2) # square the distance and add it
    return dist.item()

class Keystroke:
    def __init__(self, keyStroke : ndarray, fitness : float):
        self.keyStroke = keyStroke
        self.fitness = fitness

    # get the key stroke
    def getKeyStroke(self):
        return self.keyStroke

    # set the value of the fitness function
    # def setFitness(self, fitness: float):
    #     self.fitness = fitness

    # retrieve the value of the fitness function
    def getFitness(self) -> float:
        if self.fitness == -1:
            raise Exception("ERROR: tried to get fitness without first setting it first")
        return self.fitness

    def mutate(self, kidVector : list) -> list: # - the closer we are the less we want to change 
        maxMutation = (self.fitness / len(self.keyStroke))/4
        for i in range (len(kidVector)):
            if random.random()>0.75: # 25 percent chance to add to key
                kidVector[i] += random.random() * maxMutation
            elif random.random()>0.5: # 25 chance to mutate the other way
                kidVector[i] -= random.random() * maxMutation
        return kidVector
    # handle cross-over and mutation
    def makeChild(self, other) -> list:
        # Cross-over
        kidVector = zeros(len(self.keyStroke))
        for i in range(len(kidVector)): # kid is the average of his 2 parents
            kidVector[i] = (self.keyStroke[i] + other.getKeyStroke()[i])/2
        # and then some random add/subtract for mutation - probably base mutation on fitness 
        if random.random()>0.95: # testing out a 15% probability of a mutation
            kidVector = self.mutate(kidVector)
        return kidVector


class KeystrokeSpoofer:
     # ** get user threshold and function used to authenticate from identifier program **
    def __init__(self, numFeature : int, threshold : int,  population : int, ka : KeystrokeAuthenticator):
        self.numFeature = numFeature
        self.threshold = threshold
        self.population = population
        # self.fitnessFunction = fitnessFunction

    # Function used to create the initial guesses at the users keystroke
    # ** test vector ** will be removed later
    def createInitialPopulation(self, testVector) -> list :
        possibleKeyStroke = []
        for i in range(self.population): # randomly create possible vector in the given space
            keyStrokeVector = createSpoofVector(self.numFeature)
            # **** fitness function will come from identifier program *****
            # the test vector is inside the detector
            # keyStroke.setFitness(ka.fitnessFunction(keyStroke.getKeyStroke())) 
            keyStroke = Keystroke(keyStrokeVector, fitnessFunction(keyStrokeVector, testVector))
            possibleKeyStroke.append(keyStroke)
        KeystrokeSpoofer.sortKeyStroke(possibleKeyStroke)
        return possibleKeyStroke
    @staticmethod
    def sortKeyStroke(possibleKeyStroke : list):
        possibleKeyStroke.sort(key=lambda Keystroke : Keystroke.getFitness())
    # helper function used to create parents for generation phase
    def getMean(self, possibleKeyStroke : list) -> float:
        mean = 0
        for p in possibleKeyStroke:
            mean += p.getFitness()
        mean /= self.population
        return mean
    # helper function used to create parents for generation phase
    def getStandardDeviation(self, possibleKeyStroke : list, mean : float):
        variance = 0
        for p in possibleKeyStroke:
            variance += pow(p.getFitness()-mean,2)           
        variance /= self.population
        return math.sqrt(variance)

    def getParents(self, possibleKeyStroke : list):
        # average = self.getMean(possibleKeyStroke)
        # standardDeviation = self.getStandardDeviation(possibleKeyStroke, average)
        average = mean([ps.fitness for ps in possibleKeyStroke]).item()
        standardDeviation = std([ps.fitness for ps in possibleKeyStroke]).item()
        if standardDeviation == 0:
            return possibleKeyStroke
        parents = []
        for p in possibleKeyStroke: # a parents will be selected more depending on how close they are to the target vector
            f = p.getFitness()
            timesSelected = -round((f - average) / standardDeviation) # basically use z-score to calculate times selected
            # print("TIMES SELCTED " , timesSelected)
            # print("fitness of " , f)
            # print(" average of " , average)
            # print("standardDeviation of " , standardDeviation)

            for i in range(timesSelected):
                parents.append(p)
        # print("parent population " +(str)(len(parents)))
        while(len(parents)>self.population):
            parents.pop(-1)
        while(len(parents)<self.population):
            parents.append(possibleKeyStroke[random.randint(0,len(possibleKeyStroke)-1)])
        random.shuffle(parents)
        # for p in possibleKeyStroke:

        return parents

    # ** test vector ** will be removed later
    def getChildren(self, parents: list, testVector):
        children = []
        for i in range(len(parents)): # make all neighboring parents create children
            kidVector = parents[i].makeChild(parents[(i+1)%len(parents)])
            children.append(Keystroke(kidVector, fitnessFunction(kidVector, testVector)))
            # children.append(Keystroke(kidVector, ka.fitnessFunction(kidVector)))
        return children

    def createSpoof(self):
        # ** will use the authenticator program to test vector ** for now just use make shift function
         #  ** in actual project this will be the mean vector in the authentication program. **
        testVector = createSpoofVector(self.numFeature) 
        #  GA function 
        # 1. Create initial population
        possibleKeyStroke = self.createInitialPopulation(testVector)
        minScore = (possibleKeyStroke[0].getFitness()) # once sorted we can easily get the most fit function
        print(minScore)
        # replace with ka.passed(minScore)
        while minScore > self.threshold: # stop condition : when best guess is less then threshold
            # Selection of the best-fit individuals for next generation
            parents = self.getParents(possibleKeyStroke)
            # Generate new child by crossover and mutation operations and evaluate fitness
            children = self.getChildren(parents, testVector) # creates children using parents 
            # Replace the least-fit population with new individuals --> This isn't normally how GA works
            # ** right now I just make children the new generation  **
            possibleKeyStroke = children +parents
            KeystrokeSpoofer.sortKeyStroke(possibleKeyStroke)
            possibleKeyStroke = possibleKeyStroke[:self.population]
            minScore = possibleKeyStroke[0].getFitness() # once sorted we can easily get the most fit function
            print("Best guess score ", minScore)

        

# ** will remove from final product and move to main program
if __name__ == '__main__':
    k = KeystrokeSpoofer(31, 10, 50, None)
    k.createSpoof()