# Abdullah Arif, Clyde Rempillo, Andrew Myshok
# COMP-4800 - Selected Topic in Software engineering project
# Keystroke dynamics spoofer - a program created to spoof the keystrokes of users
# created to test the strength of various keystroke dynamic based authentication systems

import csv
from User import User
from KeystrokeAuthenticator import KeystrokeAuthenticator
from MeanBased import Euclidean, Manhattan, EuclideanNormed, ManhattanScaled
from Spoofer import KeystrokeSpoofer
from Classifier import Classifier
from numpy import asarray


class KeystrokeDynamicAttacker:
    def __init__(self, filePath: str):
        self.users = KeystrokeDynamicAttacker.createUsers(filePath)

    @staticmethod
    def createUsers(filePath: str) -> dict:
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
                    if col not in skipColumn:  # in keepColumn:
                        # print(col, ":", row[col])
                        keystroke.append(float(row[col]))
                users[userID].addKeyStroke(asarray(keystroke, dtype=float))
        for user in users.values():
            if user.getNumKeystroke != 400:
                raise Exception("We have read in", user.getNumKeystroke, "for this user")
        return users

    # get impostor data by getting the first 5 strokes of every user not counting the target user
    def getImpostorData(self, user: User) -> list:
        impostorData = []
        for u in self.users.values():
            if u == user:
                continue
            impostorData += u.getStrokes()
        return impostorData

    @staticmethod
    def getDetector(functionName: str) -> KeystrokeAuthenticator:
        detectors = {
            "Euclidean": Euclidean(),
            "Euclidean normed": EuclideanNormed(),
            "Manhattan": Manhattan(),
            "Manhattan scaled": ManhattanScaled()
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
        det = detectors.get(functionName, None)
        if det is None:
            raise ValueError("ERROR: Invalid detection method")
        return det

    def getUser(self, userID: str) -> User:
        user = self.users.get(userID, None)
        if user is None:
            raise ValueError("ERROR: We don't have a user with that id")
        return user

    def spoofUser(self, userID: str, functionName: str, population: int):
        user = self.getUser(userID)
        detector = self.getDetector(functionName)
        # impostorData = self.getImpostorData(user) #  user.getUserTestData(), impostorData
        detector.trainModel(user.getTrainingVector())
        ks = KeystrokeSpoofer(population, detector)
        ks.createSpoof()

    def classifyUsers(self, functionName: str):
        detector = KeystrokeDynamicAttacker.getDetector(functionName)
        classifier = Classifier(self.users, detector,True)
        classifier.classifyUser()


if __name__ == '__main__':
    kda = KeystrokeDynamicAttacker("Resources/DSL-StrongPasswordData.csv")
    kda.classifyUsers("Euclidean normed")
    # kda.spoofUser("s033", "Euclidean", 30)
