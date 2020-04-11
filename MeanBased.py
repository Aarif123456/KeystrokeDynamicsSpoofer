# Euclidean
# the evaluate method uses the mean vector to compare

from numpy import ndarray, zeros
from KeystrokeAuthenticator import KeystrokeAuthenticator
from math import sqrt

# class handles all classes that use a mean vector as a base for their detection model
class MeanBased(KeystrokeAuthenticator):
    def __init__(self):
        super().__init__() 
        
    # Function takes every keystroke in the training set creates a vector with the average score of all
    def trainModel(self, userTestVectors : list): 
        numFeature = len(userTestVectors[0])
        self.meanVector = zeros(numFeature)
        # feature by feature we calculate the 
        for i in range(numFeature):
            summation = 0
            for userVector in userTestVectors: 
                summation += userVector[i]
            self.meanVector[i] = (summation/len(userTestVectors))
    def getNumFeature(self) -> int:
        if self.meanVector is None:
            raise Exception("Tried getting number of features from untrained model")
        return len(self.meanVector)
    # convert distance into a measure of similarity
    def distanceToSimilarity(distance : float) -> float:
        return (1/(1+distance))
        
# implements detector based on squared Euclidean distance        
class Euclidean(MeanBased):
    def evaluate(self, testVector : ndarray) -> float:
        if len(self.meanVector) != len(testVector):
            print("mean vector:" + (str)(self.meanVector))
            print("test vector:" + (str)(testVector))
            raise Exception("ERROR: mean vector and test vector are not the same size")
        dist = 0
        for i in range(len(self.meanVector)):
            d = self.meanVector[i] - testVector[i]
            dist += pow(d, 2) # square the distance and add it
        return MeanBased.distanceToSimilarity(dist.item())


class Manhattan(MeanBased):
    def evaluate(self, testVector : ndarray) -> float:
        if len(self.meanVector) != len(testVector):
            print("mean vector:" + (str)(self.meanVector))
            print("test vector:" + (str)(testVector))
            raise Exception("ERROR: mean vector and test vector are not the same size")
        dist = 0
        for i in range(len(self.meanVector)):
            dist += abs(self.meanVector[i] - testVector[i])
        return MeanBased.distanceToSimilarity(dist.item())


# uses euclidean distance but normalizes it using the magnitude of the two vectors:
# normedDistance = euclideanDistance/(magnitudeOfMeanVector * magnitudeOfTestVector)
class EuclideanNormed(MeanBased):
    def calculateVectorMagnitude(vector : list) -> float:
        magnitude = 0 
        for a in vector:
            magnitude += pow(a,2)
        return sqrt(magnitude)

    def trainModel(self, userTestVectors : list): 
        super().trainModel(userTestVectors)
        self.meanMagnitude = EuclideanNormed.calculateVectorMagnitude(self.meanVector)

    def evaluate(self, testVector : ndarray) -> float:
        if len(self.meanVector) != len(testVector):
            print("mean vector:" + (str)(self.meanVector))
            print("test vector:" + (str)(testVector))
            raise Exception("ERROR: mean vector and test vector are not the same size")
        dist = 0
        testMagnitude = EuclideanNormed.calculateVectorMagnitude(testVector)
        for i in range(len(self.meanVector)):
            d = self.meanVector[i] - testVector[i]
            dist += (pow(d, 2)/(self.meanMagnitude*testMagnitude)) # get euclidean distance then normalize it
        return MeanBased.distanceToSimilarity(dist.item())


class ManhattanScaled(MeanBased):
    def trainModel(self, userTestVectors : list): 
        super().trainModel(userTestVectors)
        numFeature = len(userTestVectors[0])
        self.absoluteDeviation = zeros(numFeature)
        # Feature by feature we calculate the absolute deviation and then take the average
        for i in range(numFeature):
            for userVector in userTestVectors: 
                self.absoluteDeviation[i] += abs(userVector[i]-self.meanVector[i])
            self.absoluteDeviation[i] /= len(userTestVectors)

    def evaluate(self, testVector : ndarray) -> float:
        if len(self.meanVector) != len(testVector):
            print("mean vector:" + (str)(self.meanVector))
            print("test vector:" + (str)(testVector))
            raise Exception("ERROR: mean vector and test vector are not the same size")
        dist = 0
        for i in range(len(self.meanVector)):
            dist += (abs(self.meanVector[i] - testVector[i])/self.absoluteDeviation[i])
        return MeanBased.distanceToSimilarity(dist.item())
