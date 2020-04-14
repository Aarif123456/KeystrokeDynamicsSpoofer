from numpy import ndarray
import sys

if not sys.warnoptions:
    import warnings


class User:
    def __init__(self, ks=None):
        if ks is None:
            self.keyStrokes = []  # 400 keystrokes per user e.g 8 session * 50 repetition
        else:
            self.keyStrokes = ks
        self.falsePositive = 0
        self.falseNegative = 0
        self.truePositive = 0
        self.trueNegative = 0
        self.imitation = 0

    # add in the user keystrokes
    def addKeyStroke(self, keyStrokes: ndarray):
        self.keyStrokes.append(keyStrokes)

    # return the firs n keystrokes - by default it is set to 5
    def getStrokes(self, num=5) -> list:
        n = min(max(num, 0), len(self.keyStrokes))
        if n != num:
            warnings.warn("WARNING: Invalid amount of keystrokes requested " + str(num), UserWarning)
        if n == 0:
            warnings.warn("WARNING: returning no keystrokes ", UserWarning)
            return []
        return self.keyStrokes[0:n]

    # the training vector is a basically the first 10 vector 
    def getTrainingVector(self) -> list:
        return self.keyStrokes[:10]

    def setVector(self, keystroke: ndarray, num=9):
        n = min(max(num, 0), len(self.keyStrokes))
        if n != num:
            warnings.warn("WARNING: invalid index " + str(num), UserWarning)
        self.keyStrokes[n] = keystroke

    # last 10 keystrokes
    def getUserTestData(self) -> list:
        return self.keyStrokes[-10:]

    # verify all the keystroke were read
    @property
    def getNumKeystroke(self) -> int:
        return len(self.keyStrokes)

    # reset the values used to classify the users
    def resetClassifierValue(self):
        self.falsePositive = 0
        self.falseNegative = 0
        self.truePositive = 0
        self.trueNegative = 0
        self.imitation = 0

    # handle correct matches
    def accept(self, true: bool):
        if true:
            self.truePositive += 1
        else:
            self.falsePositive += 1

    # handle rejection
    def reject(self, true: bool):
        if true:
            self.trueNegative += 1
        else:
            self.falseNegative += 1

    # store successful imitation
    def imitate(self):
        self.imitation += 1

    # sheep have low error rate
    @property
    def getAccuracy(self) -> float:
        totalAttempts = self.truePositive + self.trueNegative + self.falsePositive + self.falseNegative
        totalMistakes = self.truePositive + self.trueNegative # - self.falsePositive - self.falseNegative 
        if totalAttempts == 0:
            raise Exception("ERROR: Can't calculate accuracy of model without training it")
        return totalMistakes / totalAttempts

    # used by lambs as they accept impostors
    @property
    def getFalsePositive(self) -> float:
        totalAttempts = self.truePositive + self.trueNegative + self.falsePositive + self.falseNegative
        if self.falsePositive == 0:
            return -totalAttempts #float('-inf')
        return 1-pow(self.falsePositive, -1)

    # goats have higher false negative rate
    @property
    def getFalseNegative(self) -> float:
        totalAttempts = self.truePositive + self.trueNegative + self.falsePositive + self.falseNegative
        if self.falseNegative == 0:
            return -totalAttempts #float('-inf')
        return 1-pow(self.falseNegative, -1)

    @property
    def getTruePositive(self) -> float:
        totalAttempts = self.truePositive + self.trueNegative + self.falsePositive + self.falseNegative
        if self.truePositive == 0:
            return  -totalAttempts #float('-inf')
        return 1-pow(self.truePositive, -1)

    @property
    def getTrueNegative(self) -> float:
        totalAttempts = self.truePositive + self.trueNegative + self.falsePositive + self.falseNegative
        if self.truePositive == 0:
            return  -totalAttempts #float('-inf')
        return 1-pow(self.trueNegative, -1)

    @property
    def getImitations(self) -> float:
        totalAttempts = self.truePositive + self.trueNegative + self.falsePositive + self.falseNegative
        if self.imitation == 0:
            return -totalAttempts #float('-inf')
        return 1-pow(self.imitation , -1) 
