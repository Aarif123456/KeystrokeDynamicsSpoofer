
class User():
    def __init__(self):
        self.keyStrokes = [] # 400 keystrokes per user e.g 8 session * 50 repetition
        self.resetClassifierValue()
        # 31 entries for each data entry - 3 per key: Hold, Down-Down and Up-Down
        # Hold is the time the key was pressed for and Up-Down is the time between letting go of the key and pressing the next key
        # Down-Down is the time between the time one key was pressed and second key was pressed 
        # -> So, Hold time + Up-Down time = Down-Down time
    
    # add in the user keystrokes
    def addKeyStroke(self, keyStrokes : list):
        self.keyStrokes.append(keyStrokes)

    # return the firs n keystrokes - by default it is set to 5
    def getStrokes(self, num=5) -> list:
    	num = min(max(num,0),len(self.keyStrokes))
    	return self.keyStrokes[0:num]

    # the training vector is a basically the first 200 vector - as opposed to the last 200
    def getTrainingVector(self) -> list:
    	return self.keyStrokes[:200]

    # last 200 keystrokes
    def getUserTestData(self) -> list:
    	return self.keyStrokes[200:]

    # # return how many features there are
    # def getNumFeature(self) -> int:
    #     return len(self.keyStrokes[0])

    # verify all the keystroke were read
    def verifyAllKeyRead(self) -> bool:
        return len(self.keyStrokes) == 400

    # reset the values used to classify the users
    def resetClassifierValue(self):
        self.falsePositive = 0
        self.falseNegative = 0
        self.truePositive = 0
        self.trueNegative = 0
        self.imitation = 0

    # handle correct matches
    def accept(self, true : bool):
        if true:
            self.truePositive += 1
        else:
            self.falsePositive +=1

    # handle rejection
    def reject(self, true : bool):
        if true:
            self.trueNegative += 1
        else:
            self.falseNegative +=1

    # store successful imitation
    def imitate(self):
        self.imitation +=1 

    # sheep have low error rate
    def getAccuracy(self) -> float:
        return (self.truePositive+self.trueNegative)/ (self.truePositive+self.trueNegative+self.falsePositive+self.falseNegative)
        
    # used by lambs as they accept imposters
    def getFalsePositive(self) -> int:
        return self.falsePositive
    
    # goats have higher false negative rate
    def getFalseNegative(self) -> int:
        return self.falseNegative

    def getTruePositive(self) -> int:
        return self.truePositive
    
    def getTrueNegative(self) -> int:
        return self.trueNegative

    def getImitatation(self) -> int:
        return self.imitation
