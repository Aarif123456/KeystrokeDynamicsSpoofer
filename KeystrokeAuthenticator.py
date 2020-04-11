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
        raise Exception("Tried to train abstract model!")
    @abstractmethod
    def evaluate(self, testVector : ndarray) -> int:
        raise Exception("Tried to evaluate from abstract class!")
        return -1  
    @abstractmethod
    def getNumFeature(self) -> int:
        raise Exception("Tried getting vector length from base authenticator class!")
        return -1
       

    # # ** from https://yangcha.github.io/EER-ROC/ ** 
    # def evaluateEER(user_scores, imposter_scores) -> tuple:
    #     labels = [0]*len(user_scores) + [1]*len(imposter_scores)
    #     fpr, tpr, thresholds = roc_curve(labels, user_scores + imposter_scores)
    #     # eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    #     thresh = interp1d(fpr, thresholds)(eer)
    #     return thresh


    # Training vector are the first 200 password of the user
    # User test vector is the list of the remaining 200 user attempts by the user
    # The impostor Test subjects are the first 5 passwords typed by all the impostor users (so, 50 people) 
    # return error rate and threshold
    '''def detect(self, trainingVectors : list, userTestVectors : list, imposterTestVectors : list ):
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
       # self.threshold = KeystrokeAuthenticator.evaluateEER(realUserDistance, fakeUserDistance)
       #  print("Threshold = " , self.threshold)'''
       







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








    