from numpy import ndarray, zeros, mean, std
import math
import random
from KeystrokeAuthenticator import KeystrokeAuthenticator

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

    # handle the random  mutation that occur 
    def mutate(self, kidVector : list) -> list: 
        # - the closer we are the less we want to change so we get inverse fitness score and multiply by max change in one feature
        maxMutation =(1-self.fitness)* (26 / len(self.keyStroke))
        for i in range (len(kidVector)):
            if random.random()>0.75: # 25 percent chance to add to key
                kidVector[i] += random.random() * maxMutation
            elif random.random()>0.5: # 25 chance to mutate the other way
                kidVector[i] -= random.random() * maxMutation
            kidVector[i] = abs(kidVector[i])
        return kidVector

    # handle cross-over and mutation
    def makeChild(self, other) -> list:
        # Cross-over
        kidVector = zeros(len(self.keyStroke))
        for i in range(len(kidVector)): # kid is the average of his 2 parents
            kidVector[i] = (self.keyStroke[i] + other.getKeyStroke()[i])/2
        # and then some random add/subtract for mutation - probably base mutation on fitness 
        if random.random()>0.95: # testing out a 5% probability of a mutation
            kidVector = self.mutate(kidVector)
        return kidVector


class KeystrokeSpoofer:
    def __init__(self, population : int, ka : KeystrokeAuthenticator):
        self.numFeature = ka.getNumFeature()
        self.population = population
        self.ka = ka

    # Function used to create initial spoof vector
    def createSpoofVector(self) -> ndarray:
        initialVector = zeros(self.numFeature)
        for i in range(self.numFeature):
            initialVector[i] = random.random()*26 # get random number from [0 - 26) to represent test data 
        return initialVector

    # Function used to create the initial guesses at the users keystroke
    def createInitialPopulation(self) -> list :
        possibleKeyStroke = []
        for i in range(self.population): # randomly create possible vector in the given space
            keyStrokeVector = self.createSpoofVector()
            keyStroke = Keystroke(keyStrokeVector, self.ka.evaluate( keyStrokeVector))
            possibleKeyStroke.append(keyStroke)
        KeystrokeSpoofer.sortKeyStroke(possibleKeyStroke)
        return possibleKeyStroke

    @staticmethod
    def sortKeyStroke(possibleKeyStroke : list):
        possibleKeyStroke.sort(key=lambda Keystroke : -Keystroke.getFitness())

    def getParents(self, possibleKeyStroke : list):
        average = mean([ps.fitness for ps in possibleKeyStroke]).item()
        standardDeviation = std([ps.fitness for ps in possibleKeyStroke]).item()
        parents = []
        while standardDeviation < 0.0000000001:
            # print("adding random people", standardDeviation)
            for i in range(round(self.population*.20)):
                ksv = self.createSpoofVector()
                keyStroke = Keystroke(ksv, self.ka.evaluate( ksv))
                parents.append(keyStroke) # We want to ensure this next generation is selected into the next generation
                possibleKeyStroke.append(keyStroke) # we also want to make sure the addition of these new keystroke is enough to create some variability
            average = mean([ps.fitness for ps in possibleKeyStroke]).item()
            standardDeviation = std([ps.fitness for ps in possibleKeyStroke]).item()
        
        for p in possibleKeyStroke: # a parents will be selected more depending on how close they are to the target vector
            f = p.getFitness()
            timesSelected = round((f - average) / standardDeviation) # basically use z-score to calculate times selected
            for i in range(timesSelected):
                parents.append(p)
        # KeystrokeSpoofer.sortKeyStroke(parents)
        while(len(parents)>self.population):
            parents.pop(0)
        while(len(parents)<self.population):
            parents.append(possibleKeyStroke[random.randint(0,len(possibleKeyStroke)-1)])
        return parents

    # Function used to create the children in the next generation
    def getChildren(self, parents: list):
        children = []
        random.shuffle(parents)
        for i in range(len(parents)): # make all neighboring parents create children
            kidVector = parents[i].makeChild(parents[(i+1)%len(parents)])
            children.append(Keystroke(kidVector, self.ka.evaluate(kidVector)))
        return children

    def createSpoof(self) -> int:
        #  GA function 
        # 1. Create initial population
        possibleKeyStroke = self.createInitialPopulation()
        maxScore = (possibleKeyStroke[0].getFitness()) # once sorted we can easily get the most fit function
        tries=0
        print("Initial best guess score ", maxScore)
        while maxScore < 0.85: # stop condition : when best guess is less then threshold
            # Selection of the best-fit individuals for next generation
            parents = self.getParents(possibleKeyStroke)
            # Generate new child by crossover and mutation operations and evaluate fitness
            children = self.getChildren(parents ) # creates children using parents 
            # Replace the least-fit population with new individuals 
            # by combining kid generation with parent then cutting out the bad ones
            possibleKeyStroke = children +parents 
            KeystrokeSpoofer.sortKeyStroke(possibleKeyStroke) # sort the list based on their fit
            possibleKeyStroke = possibleKeyStroke[:self.population]
            maxScore = possibleKeyStroke[0].getFitness() # once sorted we can easily get the most fit function
            tries += 1
            # print(possibleKeyStroke[0].getKeyStroke())
            print("Current best guess score ", maxScore)
        print("Successfully spoofed keystroke ")
        print("best keystroke is ", possibleKeyStroke[0].getKeyStroke())
        return tries

        

