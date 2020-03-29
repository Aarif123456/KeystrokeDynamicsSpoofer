
class User():
    def __init__(self,):
        self.keyStrokes = [] # 400 keystrokes per user e.g 8 session * 50 repetition
        # 31 entries for each data entry - 3 per key: Hold, Down-Down and Up-Down
        # Hold is the time the key was pressed for and Up-Down is the time between letting go of the key and pressing the next key
        # Down-Down is the time between the time one key was pressed and second key was pressed 
        # -> So, Hold time + Up-Down time = Down-Down time
    def addKeyStroke(self, keyStrokes : list):
        self.keyStrokes.append(keyStrokes)

    def getStrokes(self, num=5) -> list:
    	num = min(max(num,0),len(self.keyStrokes))
    	return self.keyStrokes[0:num]

    def getTrainingVector(self) -> list:
    	return self.keyStrokes[:200]

    def getUserTestData(self) -> list:
    	return self.keyStrokes[200:]

    def getNumFeature(self) -> int:
        return len(self.keyStrokes[0])

    def verifyAllKeyRead(self) -> bool:
        return len(self.keyStrokes) == 400
            