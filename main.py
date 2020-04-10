# Abdullah Arif, Clyde Rempillo, Andrew Myshok
# COMP-4800 - Selected Topic in Software engineering project
# Keystroke dynamics spoofer - a program created to spoof the keystrokes of users
# created to test the strength of various keystroke dynamic based authentication systems

# import pandas as pd
import csv
from User import User
from KeystrokeAuthenticator import KeystrokeAuthenticator
from MeanBased import Euclidean, Manhattan, EuclideanNormed, ManhattanScaled
from Spoofer import KeystrokeSpoofer
from Classifier import Classifier

class KeystrokeDynamicAttacker:
    def __init__(self, filePath : str):
        self.users = KeystrokeDynamicAttacker.createUsers(filePath)

    @staticmethod
    def createUsers(filePath : str) -> dict:
        users = dict()
        skipColumn = {"subject", "sessionIndex", "rep"}
        # keepColumn = {"H.period", "UD.period.t", "H.t", "UD.t.i", "H.i", "UD.i.e",
        #  "H.e", "UD.e.five", "H.five", "UD.five.Shift.r", "H.Shift.r","UD.Shift.r.o", "H.o",
        #    "UD.o.a", "H.a", "UD.a.n", "H.n", "UD.n.l", "H.l", "UD.l.Return", "H.Return"}
        with open(filePath, newline='') as csvfile:
            keyStrokeData = csv.DictReader(csvfile)
            # read through file
            for row in keyStrokeData:
                # we set the subject id as the dictionary key
                userID = row['subject']
                # if this is a new subject we create a new user
                if userID not in users:
                    users[userID] = User()
                keystroke = []
                for col in row:
                    if col not in skipColumn: # in keepColumn:
                        # print(col, ":", row[col])
                        keystroke.append((float)(row[col]))
                users[userID].addKeyStroke(keystroke)
        for user in users.values():
            if not user.verifyAllKeyRead():
                raise Exception("We have read in" ,  len(self.keyStrokes) , "for this user")
        return users
    
    # get impostor data by getting the first 5 strokes of every user not counting the target user
    def getImposterData(self, user : User) -> list:
        imposterData =[]
        for u in self.users.values():
            if u == user: 
                continue
            imposterData += u.getStrokes()
        return imposterData

    def getDetector(self, functionName: str) -> KeystrokeAuthenticator:
        detectors = {
        "Euclidean" : Euclidean(),
        "Euclidean normed" : EuclideanNormed(),
        "Manhattan" : Manhattan(),
        "Manhattan scaled" : ManhattanScaled()
        # "Manhattan filtered" : ManhattanFilter(),
        # "Mahalanobis" : Mahalanobis(),
        # "Mahalanobis normed" : MahalanobisNormed(),
        # "Nearest neighbor Mahalanobis" : NearestNeighborMahalanobis(),
        # "Neural network" : NeuralNetwork(),
        # "Neural network auto" : NeuralNetworkAuto(),
        # "Fuzzy logic" : FuzzyLogic(),
        # "Outlier count z-score" : OutlierCountZScore(),
        # "SVM one class" : SVMOneClass(),
        # "k-Means" : kMeans()
        }
        return detectors.get(functionName, None)

    def spoofUser(self, userID : str, functionName : str, population : int):
        user = self.users.get(userID, None)
        detector = self.getDetector(functionName)
        if user == None:
            raise Exception("ERROR: We don't have a user with that id")
        if detector == None:
            raise Exception("ERROR: Invalid detection method")
        
        # imposterData = self.getImposterData(user) #  user.getUserTestData(), imposterData
        detector.trainModel(user.getTrainingVector())
        ks = KeystrokeSpoofer(user.getNumFeature(), population , detector)
        ks.createSpoof()
        
    def classifyUsers(self, functionName : str):
        detector = self.getDetector(functionName)
        classifier = Classifier(self.users, detector)
        classifier.classifyUser()

if __name__ == '__main__':
    kda = KeystrokeDynamicAttacker("Resources/DSL-StrongPasswordData.csv")
    kda.classifyUsers("Euclidean normed")
