# Abdullah Arif, Clyde Rempillo, Andrew Myshok
# COMP-4800 - Selected Topic in Software engineering project
# Keystroke dynamics user classifier - trying to classify users based on the difference of their authentication
from KeystrokeAuthenticator import KeystrokeAuthenticator
from statistics import stdev, mean
from numpy import percentile
# from pprint import pprint

class Classifier:
    def __init__(self, users: dict, userModel: KeystrokeAuthenticator, comparative = False):
        self.users = users
        self.userModel = userModel
        # comparative means it determine the threshold based on the given population otherwise it will use a segment user
        self.comparative = comparative
    @staticmethod
    def findOutlier(scores: list, userIDs: list) -> list:
        avg = mean(scores)
        std = stdev(scores)
        # basically get every user with z-score above 3
        return [userIDs[i] for i in range(len(scores)) if (scores[i] - avg) > std * 3]

    def classifyUser(self):
        # build the users values needed to classify the users
        self.buildClassifier()
        userIDs = list(self.users.keys())
        # classify user based on their relative performance
        # get sheep from data
        if self.comparative:
            sheepScore = [self.users[userID].getAccuracy for userID in userIDs ]
            sheepThreshold =  percentile(sheepScore,70)
            print("percentile =", sheepThreshold)
            # pprint(sheepScore)
        else:
            sheepThreshold = 0.8
        sheepIDs = [userID for userID in userIDs if self.users[userID].getAccuracy >= sheepThreshold]
       
        if len(sheepIDs) != 0:
            print("The following user are considered to be sheep:", sheepIDs)
        else:
            print("There are no sheep in the data... ")
        
        # determine the lamb from the data
        if self.comparative:
            lambScores = [self.users[userID].getFalsePositive for userID in userIDs ]
            lambThreshold =  percentile(lambScores,90)
            print("percentile =", lambThreshold)
            # pprint(lambScores)
        else:
            lambThreshold = 0.99
        lambsIDs = [userID for userID in userIDs if self.users[userID].getFalsePositive > lambThreshold ]
        if len(lambsIDs) != 0:
            print("The following user are considered to be lamb:", lambsIDs)
        else:
            print("There are no lambs in the data... ")

        # determine the goat from the data
        if self.comparative:
            goatScores = [self.users[userID].getFalseNegative for userID in userIDs ]
            goatThreshold =  percentile(goatScores,90)
            print("percentile =", goatThreshold)
            # pprint(goatScores)
        else:
            goatThreshold = 0.99
        goatsIDs = [userID for userID in userIDs if self.users[userID].getFalseNegative  > goatThreshold]
        if len(goatsIDs) != 0:
            print("The following user are considered to be goat:", goatsIDs)
        else:
            print("There are no goats in the data... ")

        # determine the wolf from the data
        if self.comparative:
            wolfScores = [self.users[userID].getImitations for userID in userIDs ]
            wolfThreshold =  percentile(wolfScores,90)
            print("percentile =", wolfThreshold)
            # pprint(wolfScores)
        else:
            wolfThreshold = 0.99
       
        wolvesIDs = [userID for userID in userIDs if self.users[userID].getImitations >wolfThreshold]
        if len(wolvesIDs) != 0:
            print("The following user are considered to be wolf:", wolvesIDs)
        else:
            print("There are no wolves in the data... ")
        return len(sheepIDs), len(lambsIDs), len(goatsIDs), len(wolvesIDs)

    # get the information needed to classify the users
    def buildClassifier(self):
        for userID in self.users:
            self.trainUser(userID)
            self.checkSelf(userID)
            self.checkImpostor(userID)

    # Step 1 (training): Use the first 200 passwords typed by the genuine user and train model to detect user
    def trainUser(self, userID: str):
        user = self.users[userID]
        self.userModel.trainModel(user.getTrainingVector())
        # reset the value that will be used to classify user in case model is run multiple time
        user.resetClassifierValue()

    # Step 2 (genuine-user testing): Next see how well detector does against user's own results
    def checkSelf(self, userID: str):
        user = self.users[userID]
        userTestVectors = user.getUserTestData()
        for testVector in userTestVectors:
            # Calculate the distance between the test vector and the mean vector and square it
            if self.userModel.evaluate(testVector) < 0.85:  # user failed own test
                user.reject(False)  # store false rejection - rejected themselves
            else:
                user.accept(True)  # store true match - authenticated themselves

    # Step 3 (impostor testing): Check how model does against impostor score 
    def checkImpostor(self, userID: str):
        user = self.users[userID]
        for impostorID in self.users.keys():
            if impostorID == userID:  # the user themselves are not an impostor
                continue
            impostor = self.users[impostorID]
            for testVector in impostor.getStrokes(10):
                if self.userModel.evaluate(testVector) < 0.85:  # impostor failing test
                    user.reject(True)  # store true rejection - rejected an impostor
                else:
                    user.accept(False)  # store true match
                    impostor.imitate()  # store the
