# Abdullah Arif, Clyde Rempillo, Andrew Myshok
# COMP-4800 - Selected Topic in Software engineering project
# Keystroke dynamics spoofer - a program created to spoof the keystrokes of users
# created to test the strength of various keystroke dynamic based authentication systems

# '''
class KeystrokeDynamicAttacker:
    def __init__(self):
        # For every users creates user and store all their Keystrokes
        #  self.reader = self.loadCSV(fileName)

    @staticmethod
    def loadCSV(fileName : str):
        with open(fileName, newline='') as csvfile:
            return csv.DictReader(csvfile)
            # for row in reader:
                # print(row['first_name'], row['last_name'])

            # data = list(csv.reader(csvfile))
    
    

# if __name__ == '__main__':

'''
 Detector = {"Euclidean" : Euclidean(),
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