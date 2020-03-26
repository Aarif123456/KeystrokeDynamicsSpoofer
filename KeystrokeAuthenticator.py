# Abdullah Arif
# Program created to identify use based on their keystroke 
# reference
# 14 algorithms based on - https://www.cs.cmu.edu/~maxion/pubs/KillourhyMaxion09.pdf
# Awesome guide - https://appliedmachinelearning.blog/2017/07/26/user-verification-based-on-keystroke-dynamics-python-code/ 

# imports
import pandas as pd
import numpy as np
from scipy.optimize import brentq
from scipy.interpolate import interp1d
class KeystrokeAuthenticator:
    def __init__(self, fileName : str):
        self.reader = KeystrokeAuthenticator.loadCSV(fileName)
        for row in reader:
            print(row['first_name'], row['last_name'])

    @staticmethod
    def loadCSV(fileName : str):
        with open(fileName, newline='') as csvfile:
            return csv.DictReader(csvfile)
            # data = list(csv.reader(csvfile))
            

class User():
    def __init__(self):
        # array of 8 for 8 sessions
        # each array 50 array inside for each repetition 
        # 30 entries for each data entry - 3 per key: Hold, Down-Down and Up-Down
        # Hold is the time the key was pressed for and Up-Down is the time between letting go of the key and pressing the next key
        # Down-Down is the time between the time one key was pressed and second key was pressed 
        # -> So, Hold time + Up-Down time = Down-Down time


# Step 1 (training): Retrieve the first 200 passwords typed by the genuine user from the password-timing table. Use the anomaly detector's training function with these password-typing times to build a detection model for the user's typing.

# Step 2 (genuine-user testing): Retrieve the last 200 passwords typed by the genuine user from the password-timing table. Use the anomaly detector's scoring function and the detection model (from Step 1) to generate anomaly scores for these password-typing times. Record these anomaly scores as user scores.

# Step 3 (impostor testing): Retrieve the first 5 passwords typed by each of the 50 impostors (i.e., all subjects other than the genuine user) from the password-timing table. Use the anomaly detector's scoring function and the detection model (from Step 1) to generate anomaly scores for these password-typing times. Record these anomaly scores as impostor scores.

# Step 4 (assessing performance): Employ the user scores and impostor scores to generate an ROC curve for the genuine user. Calculate, from the ROC curve, an equal-error rate, that is, the error rate corresponding to the point on the curve where the false-alarm (false-positive) rate and the miss (false-negative) rate are equal.

# Repeat the above four steps, designating each of the subjects as the genuine user in turn, and calculating the equal-error rate for the genuine user. Calculate the mean of all 51 subjects' equal-error rates as a measure of the detector's performance, and calculate the standard deviation as a measure of its variance across subjects. 

# The detectors use various algorithm to determine a threshold where either 
# 1. The false-positive rate = false-negative (Equal-Error rate)
# 2. We reduce the total number of error: zero-miss false-alarm rate

def Detect(functionName) -> tuple:
    #  Might be able to everything in one function
    Just make a list of function in adictionary and return different value
# For every feature calculate the mean for every feature
def calculateMean(featureTimes : list) -> int:
    sum = 0
    for time in featureTimes:
        sum += time
    sum = sum/len(featureTimes)
    
''' 
Function takes in the feature matrix per user and creates a mean vector
The feature matrix is a collection of the list that contains all the times 
for the given feature for the given user 
'''
def createMeanVector(featureMatrix : list) -> list: 
    meanVector = []
    for featureTimes in featureMatrix: 
        meanVector.append(calculateMean(featureTimes))
    return meanVector
    # for every feature get the mean and put it in dictionary
def EuclideanTest(meanVector : list, testVector : list) -> int:
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

# ** from https://yangcha.github.io/EER-ROC/ ** 
def evaluateEER(user_scores, imposter_scores) -> tuple:
    labels = [0]*len(user_scores) + [1]*len(imposter_scores)
    fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
    eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    thresh = interp1d(fpr, thresholds)(eer)
    return (eer, thresh)

# calculate from frp and tpr zero miss false positive rate
def evaluteZMFPR(fpr : int, tpr : int): 
    missRate = 1-tpr
    return fpr+missRate

# calculate zero miss false positive rate from data ** NEEDS TO BE TESTED **
def evaluteZMFPR(user_scores, imposter_scores) -> tuple:
    labels = [0]*len(user_scores) + [1]*len(imposter_scores)
    fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
    minIndex = 0
    for i in range(1, len(thresholds)):
        if(evaluteZMFPR(fpr[i],tpr[i]) < evaluteZMFPR(fpr[minIndex],tpr[minIndex])):
            minIndex = i
    return (evaluteZMFPR(fpr[minIndex],tpr[minIndex]), thresholds[i])


# Detection using basic Euclidean algorithm 
def Euclidean(self, featureMatrix : list, imposterTestVector : list, userTestVector : list) -> int:
    # Training create a vector with the mean of each feature
    meanVector = createMeanVector(featureMatrix)
    # Testing 
    realUserDistance = []
    for testVector in userTestVector: 
        # Calculate the distance between the test vector and the mean vector and square it
        realUserDistance.append(EuclideanTest(meanVector, testVector))
    fakeUserDistance = []
    for testVector in impostorTestVector
        fakeUserDistance.append(EuclideanTest(meanVector, testVector))
    if self.EERMode: # get EER score
        return evaluateEER(realUserDistance, fakeUserDistance)
    return evaluteZMFPR(realUserDistance, fakeUserDistance)


def EuclideanNormed():

def Manhattan():

def ManhattanFilter():

def ManhattanScaled():

def Mahalanobis():

def MahalanobisNormed():

def NearestNeighborMahalanobis():

def NeuralNetwork():

def NeuralNetworkAuto():

def FuzzyLogic():

def OutlierCountZScore():

def SVMOneClass():

def kMeans():

