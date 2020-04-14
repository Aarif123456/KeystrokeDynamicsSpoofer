# Abdullah Arif
# Program created to identify use based on their keystroke

# imports 
from numpy import ndarray
from abc import ABC, abstractmethod  # Make class abstract


class KeystrokeAuthenticator(ABC):
    def __init__(self):
        self.threshold = -1

    @abstractmethod
    def trainModel(self, userVectors: list):
        raise Exception("Tried to train abstract model!")

    @abstractmethod
    def evaluate(self, testVector: ndarray) -> int:
        raise Exception("Tried to evaluate from abstract class!")

    @abstractmethod
    def getNumFeature(self) -> int:
        raise Exception("Tried getting vector length from base authenticator class!")

    # # ** from https://yangcha.github.io/EER-ROC/ ** 
    # def evaluateEER(user_scores, impostor_scores) -> tuple:
    #     labels = [0]*len(user_scores) + [1]*len(impostor_scores)
    #     fpr, tpr, thresholds = roc_curve(labels, user_scores + impostor_scores)
    #     # eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    #     thresh = interp1d(fpr, thresholds)(eer)
    #     return thresh

    # Training vector are the first 200 password of the user
    # User test vector is the list of the remaining 200 user attempts by the user
    # The impostor Test subjects are the first 5 passwords typed by all the impostor users (so, 50 people) 
    # return error rate and threshold
    '''def detect(self, trainingVectors : list, userTestVectors : list, impostorTestVectors : list ):
        # Step 1 (training): USe the first 200 passwords typed by the genuine user and train model to detect user
        self.trainModel(trainingVectors)
        # Step 2 (genuine-user testing): Next see how well detector does against user's own results
        realUserDistance = []
        for testVector in userTestVectors: 
            # Calculate the distance between the test vector and the mean vector and square it
            realUserDistance.append(self.evaluate( testVector))
        # Step 3 (impostor testing): Check how model does against impostor score 
        fakeUserDistance = []
        for testVector in impostorTestVectors:
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
