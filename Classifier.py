# Abdullah Arif, Clyde Rempillo, Andrew Myshok
# COMP-4800 - Selected Topic in Software engineering project
# Keystroke dynamics user classifier - trying to classify users based on the difference of their authentication
from KeystrokeAuthenticator import KeystrokeAuthenticator
# from copy import deepcopy
from statistics import stdev ,mean
import numpy as np
class Classifier:
    def __init__(self, users : list, userModel : KeystrokeAuthenticator):
        self.users = users
        self.userModel = userModel

    def findOutlier(scores : list, userIDs : list) -> int:
        avg = mean(scores)
        std = stdev(scores)
        # basically get every user with z-score above 3
        return [userIDs[i] for i in range(len(scores)) if (scores[i]-avg)> std*3]

    def classifyUser(self):
        # build the users values needed to classify the users
        self.buildClassifier()
        userIDs = list(self.users.keys())
        # classify user based on their relative performance
        # ** ASSUMMING ALL DATA IS NORMALLY DISTRIBUTED otherwise we can't use the z-score to determine outliers **

        # get sheep from data
        notSheepScore = [(1-self.users[userID].getAccuracy()) for userID in userIDs]
        notSheepIDs = set(Classifier.findOutlier(notSheepScore, userIDs))
        sheepIDs = [userID for userID in userIDs if userID not in notSheepIDs]
        if len(sheepIDs)!= 0:
            print("The following user are considered to be sheep:", sheepIDs)
        else:
            print("There are no sheep in the data... ")
        
        # determine the lamb from the data
        lambScores = [self.users[userID].getFalsePositive() for userID in userIDs]
        lambsIDs = Classifier.findOutlier(lambScores, userIDs)
        if len(lambsIDs)!= 0:
            print("The following user are considered to be lamb:", lambsIDs)
        else:
            print("There are no lambs in the data... ")
        
        # determine the goat from the data
        goatScores =  [self.users[userID].getFalseNegative() for userID in userIDs]
        goatsIDs = Classifier.findOutlier(goatScores, userIDs)
        if len(goatsIDs)!= 0:
            print("The following user are considered to be goat:", goatsIDs)
        else:
            print("There are no goats in the data... ")
        
        # determine the wolf from the data
        wolfScores =  [self.users[userID].getImitatation() for userID in userIDs]
        wolvesIDs = Classifier.findOutlier(wolfScores, userIDs)
        if len(wolvesIDs)!= 0:
            print("The following user are considered to be wolf:", wolvesIDs)
        else:
            print("There are no wolves in the data... ")
        
    # get the information needed to classify the users
    def buildClassifier(self):
        for userID in self.users:
            self.trainUser(userID)
            self.checkSelf(userID)
            self.checkImposter(userID)

    # Step 1 (training): Use the first 200 passwords typed by the genuine user and train model to detect user
    def trainUser(self, userID : str):
        user = self.users[userID]
        self.userModel.trainModel(user.getTrainingVector())
        user.resetClassifierValue() # reset the value that will be used to classify user in case model is run multiple time

    # Step 2 (genuine-user testing): Next see how well detector does against user's own results
    def checkSelf(self, userID : str):
        user = self.users[userID]
        userTestVectors = user.getUserTestData()
        for testVector in userTestVectors: 
            # Calculate the distance between the test vector and the mean vector and square it
            if self.userModel.evaluate( testVector)<0.85: # user failed own test
                user.reject(False) # store false rejection - rejected themselves
            else:
                user.accept(True) # store true match - authenticated themselves

    # Step 3 (impostor testing): Check how model does against impostor score 
    def checkImposter(self, userID : str):
        user = self.users[userID]
        for imposterID in self.users.keys():
            if imposterID == userID: # the user themselves are not an imposter
                continue
            imposter = self.users[imposterID]
            for testVector in imposter.getStrokes(5):
                if self.userModel.evaluate( testVector)<0.85: # imposter failing test
                    user.reject(True) # store true rejection - rejected an imposter
                else:
                    user.accept(False) # store true match
                    imposter.imitate() # store the 

# *8Things to look at if our data wasn't normally distributed - Shapiro-Wilk test p-value above 0.05 - kurtosis z-score should between -1.96-1.96
 # def t_test(sample, mu):
    #     mean = np.mean(sample)
    #     var = np.var(sample, ddof = 1) ###
    #     sem = (var / len(sample)) ** .5
    #     t = abs(mu - mean)/sem
    #     df = len(sample) - 1
    #     p = 2*(1-scs.t.cdf(t, df)) ###
    # return (t, p)
           
