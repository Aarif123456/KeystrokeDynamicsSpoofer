# Abdullah Arif, Clyde Rempillo, Andrew Myshok
# COMP-4800 - Selected Topic in Software engineering project
# Keystroke dynamics spoofer - a program created to spoof the keystrokes of users
# created to test the strength of various keystroke dynamic based authentication systems

# import pandas as pd
import csv
from User import User
from Euclidean import Euclidean
from Spoofer import KeystrokeSpoofer
class KeystrokeDynamicAttacker:
    def __init__(self, filePath : str):
        self.users = KeystrokeDynamicAttacker.createUsers(filePath)

    @staticmethod
    def createUsers(filePath : str) -> dict:
        users = dict()
        skipColumn = {"subject", "sessionIndex", "rep"}
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
                    if col not in skipColumn:
                        # print(col, ":", row[col])
                        keystroke.append((float)(row[col]))
                users[userID].addKeyStroke(keystroke)
        for user in users.values():
            if not user.verifyAllKeyRead():
                raise Exception("We have read in" ,  len(self.keyStrokes) , "for this user")



        # keyStrokeData = pd.read_csv(filePath)
        # Test with down-to down column gone and see how it affect the accuracy  
        # keepColumns = ["subject", "sessionIndex", "rep", "H.period", "UD.period.t", "H.t", "UD.t.i", "H.i", "UD.i.e", "H.e", "UD.e.five", "H.five", "UD.five.Shift.r", "H.Shift.r", "UD.Shift.r.o", "H.o", "UD.o.a", "H.a", "UD.a.n", "H.n", "UD.n.l", "H.l", "UD.l.Return", "H.Return"]
        #  keyStrokeData = pd.read_csv(filePath,  usecols = keepColumns )

        # userIds = keyStrokeData["subject"].unique()
        # for userID in userIds:
        #     userKeyStroke = keyStrokeData.loc[keyStrokeData.subject == userID, "H.period":"H.Return"]
        #     users[userID] = User(userKeyStroke)
        return users
    
    # get impostor data by getting the first 5 strokes of every user not counting the target user
    def getImposterData(self, user : User) -> list:
        imposterData =[]
        for u in self.users.values():
            if u == user: 
                continue
            imposterData += u.getStrokes()
        return imposterData

    def checkUserCategory(self, userID : str, functionName : str, population : int):
        if userID not in self.users:
            raise Exception("ERROR: We don't have a user with that id")
        if functionName == "Euclidean":
            detector = Euclidean()
        else:
             raise Exception("ERROR: Invalid detection method")
        user = self.users[userID]
        imposterData = self.getImposterData(user)
        detector.detect(user.getTrainingVector(), user.getUserTestData(), imposterData)
        ks = KeystrokeSpoofer(user.getNumFeature(), population , detector)
        ks.createSpoof()
        print(user.getStrokes(1))

if __name__ == '__main__':
    kda = KeystrokeDynamicAttacker("Resources/DSL-StrongPasswordData.csv")
    kda.checkUserCategory("s002", "Euclidean", 30)

'''
 detector = {"Euclidean" : Euclidean(),
                        "EuclideanNormed" : EuclideanNormed(),
                        "Manhattan" : Manhattan(),
                        "ManhattanFilter" : ManhattanFilter(),
                        "ManhattanScaled" : ManhattanScaled(),
                        "Mahalanobis" : Mahalanobis(),
                        "MahalanobisNormed" : MahalanobisNormed(),
                        "NearestNeighborMahalanobis" : NearestNeighborMahalanobis(),
                        "NeuralNetwork" : NeuralNetwork(),
                        "NeuralNetworkAuto" : NeuralNetworkAuto(),
                        "FuzzyLogic" : FuzzyLogic(),
                        "OutlierCountZScore" : OutlierCountZScore(),
                        "SVMOneClass" : SVMOneClass(),
                        "kMeans" : kMeans()
        }
        '''