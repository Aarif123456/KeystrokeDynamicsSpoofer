# Abdullah Arif
# Program created to identify use based on their keystroke 
# reference
# 14 algorithms based on - https://www.cs.cmu.edu/~maxion/pubs/KillourhyMaxion09.pdf
# Awesome guide - https://appliedmachinelearning.blog/2017/07/26/user-verification-based-on-keystroke-dynamics-python-code/ 

# imports
from numpy import ndarray #, argmin, argmax
from scipy.optimize import brentq
from scipy.interpolate import interp1d
from sklearn.metrics import roc_curve
from abc import ABC, abstractmethod  # Make class abstract

class KeystrokeAuthenticator(ABC):
    def __init__(self):
       self.threshold = -1

    @abstractmethod   
    def trainModel(self, userVector : ndarray):
        pass
    @abstractmethod
    def evaluate(self, meanVector : ndarray, testVector : ndarray) -> int:
        raise Exception("Tried to evaluate from abstract class!")
        return -1


    # The detectors use various algorithm to determine a threshold where either 
    # 1. The false-positive rate = false-negative (Equal-Error rate)
    # 2. We reduce the total number of error: zero-miss false-alarm rate

    # ** from https://yangcha.github.io/EER-ROC/ ** 
    def evaluateEER(user_scores, imposter_scores) -> tuple:
        labels = [0]*len(user_scores) + [1]*len(imposter_scores)
        fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
        eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
        thresh = interp1d(fpr, thresholds)(eer)
        return (eer, thresh)

    # def evaluateEER(user_scores, imposter_scores):
    #     labels = [0]*len(user_scores) + [1]*len(imposter_scores)
    #     fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
    #     missrates = 1 - tpr
    #     farates = fpr

    #     dists = missrates - farates
    #     idx1 = argmin(dists[dists >= 0])
    #     idx2 = argmax(dists[dists < 0])
    #     x = [missrates[idx1], farates[idx1]]
    #     y = [missrates[idx2], farates[idx2]]
    #     a = ( x[0] - x[1] ) / ( y[1] - x[1] - y[0] + x[0] )
    #     eer = x[0] + a * ( y[0] - x[0] )
    #     return (eer, thresholds )
    '''  ** NEEDS TO BE TESTED **  
    # calculate from frp and tpr zero miss false positive rate
    def evaluateZMFPR(fpr : int, tpr : int) -> int: 
        missRate = 1-tpr
        return fpr+missRate

    # calculate zero miss false positive rate from data 
    def evaluateZMFPR(user_scores, imposter_scores) -> tuple:
        labels = [0]*len(user_scores) + [1]*len(imposter_scores)
        fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
        minIndex = 0
        for i in range(1, len(thresholds)):
            if(evaluateZMFPR(fpr[i],tpr[i]) < evaluateZMFPR(fpr[minIndex],tpr[minIndex])):
                minIndex = i
        return (evaluateZMFPR(fpr[minIndex],tpr[minIndex]), thresholds[i])
    '''


    # Training vector are the first 200 password of the user
    # User test vector is the list of the remaining 200 user attempts by the user
    # The impostor Test subjects are the first 5 passwords typed by all the impostor users (so, 50 people) 
    # return error rate and threshold
    def detect(self, trainingVectors : list, userTestVectors : list, imposterTestVectors : list ):
        # Step 1 (training): USe the first 200 passwords typed by the genuine user and train model to detect user
        self.trainModel(trainingVectors)
        # Step 2 (genuine-user testing): Next see how well detector does against user's own results
        realUserDistance = []
        for testVector in userTestVectors: 
            # Calculate the distance between the test vector and the mean vector and square it
            realUserDistance.append(self.evaluate( testVector))
        # Step 3 (impostor testing): Check how model does against impostor score 
        fakeUserDistance = []
        for testVector in imposterTestVectors:
            fakeUserDistance.append(self.evaluate(testVector))
        # Step 4 (assessing performance): Get how well the model did
        # if self.EERMode: # get EER score
        self.EER, self.threshold = KeystrokeAuthenticator.evaluateEER(realUserDistance, fakeUserDistance)
        print("EER = " ,self.EER)
        print("Threshold = " , self.threshold)
        # might just remove score later -> good way to make sure we implemented function correctly
        # ***** NEED TO IMPLEMENT LATER **********
        # return KeystrokeAuthenticator.evaluateZMFPR(realUserDistance, fakeUserDistance)

    







# def ManhattanFilter():

# def Mahalanobis():

# def MahalanobisNormed():

# def NearestNeighborMahalanobis():

# def NeuralNetwork():

# def NeuralNetworkAuto():

# def FuzzyLogic():

# def OutlierCountZScore():

# def SVMOneClass():

# def kMeans():








    