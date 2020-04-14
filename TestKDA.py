# Abdullah Arif 
# program created to test the functionality of the spoofer program
import random
import unittest
import numpy as np
from copy import deepcopy
from Classifier import Classifier
from Spoofer import KeystrokeSpoofer, Keystroke
from User import User
from main import KeystrokeDynamicAttacker
from MeanBased import Euclidean


class TestAuthenticator(unittest.TestCase):
    validFunction = ["Euclidean", "Euclidean normed", "Manhattan", "Manhattan scaled"]
    invalidFunction = "I am not a function"
    validUser = ["s022", "s033"]
    invalidUser = "s001"

    def setUp(self):
        self.kda = KeystrokeDynamicAttacker("Resources/DSL-StrongPasswordData.csv")

    def test_keystroke_similarity(self):
        print("Testing similarity rating on evaluators")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        fakeKeystroke = np.full(31, 50)
        for functionName in TestAuthenticator.validFunction:
            detector = KeystrokeDynamicAttacker.getDetector(functionName)
            detector.trainModel(user.getTrainingVector())
            # Fake should be less similar then the real user keystroke
            self.assertTrue(detector.evaluate(fakeKeystroke) < detector.evaluate(user.getStrokes(1)[0]))

    # test the model using one keystroke as it should give us back a perfect match
    def test_model_one_stroke(self):
        print("Testing by training model with one keystroke")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        for functionName in TestAuthenticator.validFunction:
            detector = KeystrokeDynamicAttacker.getDetector(functionName)
            detector.trainModel(user.getStrokes(1))
            self.assertEqual(detector.evaluate(user.getStrokes(1)[0]), 1)

    # Test positive value as population
    def test_positive_population(self):
        print("Testing model using a valid population")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        functionName = TestAuthenticator.validFunction[0]
        detector = KeystrokeDynamicAttacker.getDetector(functionName)
        detector.trainModel(user.getStrokes(1))
        print(user.getStrokes(1))
        spoofer = KeystrokeSpoofer(100, detector)
        self.assertTrue(len(spoofer.createSpoof()) > 0)

    # Test positive value as population
    def test_negative_population(self):
        print("Testing by trying to set a negative population")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        functionName = TestAuthenticator.validFunction[0]
        detector = KeystrokeDynamicAttacker.getDetector(functionName)
        detector.trainModel(user.getStrokes(1))
        with self.assertRaises(ValueError):
            spoofer = KeystrokeSpoofer(-100, detector)
            spoofer.createSpoof()

    # Test with 0 as a population
    def test_zero_population(self):
        print("Testing by trying to setting population to zero")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        functionName = TestAuthenticator.validFunction[0]
        detector = KeystrokeDynamicAttacker.getDetector(functionName)
        detector.trainModel(user.getStrokes(1))
        with self.assertRaises(ValueError):
            spoofer = KeystrokeSpoofer(0, detector)
            spoofer.createSpoof()

    def test_floating_population(self):
        print("Test spoofing using a fraction as a population ")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        functionName = TestAuthenticator.validFunction[0]
        detector = KeystrokeDynamicAttacker.getDetector(functionName)
        detector.trainModel(user.getStrokes(1))
        with self.assertWarns(UserWarning):
            spoofer = KeystrokeSpoofer(20.3423, detector)
            spoofer.createSpoof()

    def test_invalid_type_population(self):
        print("Test spoofing using a nonsensical string ")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        functionName = TestAuthenticator.validFunction[0]
        detector = KeystrokeDynamicAttacker.getDetector(functionName)
        detector.trainModel(user.getStrokes(1))
        with self.assertRaises(TypeError):
            spoofer = KeystrokeSpoofer("Something between 2 and 7 ", detector)
            spoofer.createSpoof()

    def test_valid_keystroke_getter(self):
        print("Test to get make sure keystroke getter works ")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        self.assertEqual(len(user.getStrokes(10)), 10)

    def test_negative_keystroke_getter(self):
        print("Try getting back negative keystrokes ")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        with self.assertWarns(UserWarning):
            self.assertEqual(len(user.getStrokes(-100)), 0)

    def test_out_of_bound_keystroke_getter(self):
        print("Try getting more keystrokes then is available ")
        user = self.kda.getUser(TestAuthenticator.validUser[0])
        with self.assertWarns(UserWarning):
            self.assertEqual(len(user.getStrokes(1000)), 400)

    def test_making_children(self):
        print("Seeing the result of making kids ")
        # make an ultra-fit parent with [0, 0, 0] as keystroke
        parent1 = Keystroke(np.zeros(3), 1)
        # make an ultra-fit parent with [5, 5, 5] as keystroke
        parent2 = Keystroke(np.full(3, 5), 1)
        perfectKid = np.full(3, 5)
        # 10000 is being dramatic because there is a 5% chance of mutation
        # But, with perfects who are perfectly fit we should have no mutation
        for i in range(10000):
            self.assertTrue((parent1.makeChild(parent2) - perfectKid).all())
            self.assertTrue((parent2.makeChild(parent1) - perfectKid).all())

    def test_invalid_user_main(self):
        print("Test main with an invalid user ")
        with self.assertRaises(ValueError):
            self.kda.spoofUser(TestAuthenticator.invalidUser, TestAuthenticator.validFunction[0], 20)

    def test_invalid_spoof_function_main(self):
        print("Test main with invalid function for evaluation ")
        with self.assertRaises(ValueError):
            self.kda.spoofUser(TestAuthenticator.validUser[0], TestAuthenticator.invalidFunction, 20)

    def test_invalid_classify_function_main(self):
        print("Test main with invalid function for evaluation ")
        with self.assertRaises(ValueError):
            self.kda.classifyUsers(TestAuthenticator.invalidFunction)

    # test detection of obvious goats
    def testGoat(self):
        print("Test if classifier can detect goats amidst group of sheep")
        sheep = AnimalCreator.create_sheep(200)
        goat = AnimalCreator.create_goat(2)
        # add the goats to the sheep
        sheep.update(goat)
        detector = self.kda.getDetector("Manhattan")
        classifier = Classifier(sheep, detector, True)
        sheepIDs, lambsIDs, goatsIDs, wolvesIDs = classifier.classifyUser()
        self.assertEqual(sheepIDs, 200)
        # self.assertEqual(lambsIDs, 0) # can't guarantee
        self.assertEqual(goatsIDs, 2)
        # self.assertEqual(wolvesIDs, 0)

    # test detection of obvious wolf and lambs
    def test_wolf_and_lamb(self):
        print("Test if classifier can detect lambs and wolves")
        sheep = AnimalCreator.create_sheep(400)
        animal = AnimalCreator.create_lambs_and_wolves(2)
        goat = AnimalCreator.create_goat(5)
        # add the animals to the sheep
        animal.update(sheep)
        animal.update(goat)
        detector = self.kda.getDetector("Manhattan")
        classifier = Classifier(animal, detector, True)
        sheepIDs, lambsIDs, goatsIDs, wolvesIDs = classifier.classifyUser()
        self.assertTrue(400 <= sheepIDs <= 406)
        self.assertEqual(lambsIDs, 4)
        self.assertEqual(goatsIDs, 5)
        self.assertEqual(wolvesIDs, 2)


# Class to make sets that represent different type of users
class AnimalCreator:
    @staticmethod
    def dict2lst(prefix: str, lst: list):
        return {prefix + str(i): lst[i] for i in range(len(lst))}

    # Make super sheep who have identical keystrokes so their match is always perfect
    # num is the number of sheep created
    # repeated is the number of keystroke per user
    # size is how big the array than holds the keystroke data is supposed to be
    @staticmethod
    def create_sheep(num: int, repeated=400, size=31) -> dict:
        sheep_ks = [np.random.rand(size) for _ in range(num)]
        return AnimalCreator.dict2lst("sheep", [User([deepcopy(sk) for _ in range(repeated)]) for sk in sheep_ks])

    # same parameter as the create_sheep function - create a super random user that is prone to rejecting themselves
    @staticmethod
    def create_goat(num: int, repeated=400, size=31) -> dict:
        return AnimalCreator.dict2lst("goat", [
            User([(np.random.rand(size)) for __ in range(repeated)]) for _ in range(num)])

    @staticmethod
    def create_lambs_and_wolves(num: int, repeated=400, size=31) -> dict:
        if repeated < 12:
            raise ValueError("For this little hack to work the you need more than 11 values for the keystrokes")
        lamb1Stroke = AnimalCreator.create_sheep(num, repeated, size)
        maxDistancePerStroke = (0.15 / 0.86) / size
        wolfStroke = []
        lamb2Stroke = []
        for wf in lamb1Stroke.values():
            wolfUser = User()
            lamb2User = User()
            for j in range(repeated):
                wolfUser.addKeyStroke(np.asarray([maxDistancePerStroke + w for w in wf.getStrokes(repeated)[j]]))
                lamb2User.addKeyStroke(np.asarray([maxDistancePerStroke * 2 + w for w in wf.getStrokes(repeated)[j]]))
            wolfStroke.append(wolfUser)
            lamb2Stroke.append(lamb2User)
        # combine lamb strokes
        lambStroke = list(lamb1Stroke.values()) + lamb2Stroke
        lambStroke = AnimalCreator.dict2lst("lamb", lambStroke)
        # make wolf seem adaptable - they are able to vary their keystroke
        for wolf in wolfStroke:
            # 5 - 10 are elements in the training vector that are not in the test data
            for i in range(5, 10):
                wolf.setVector(wolf.getStrokes(repeated)[i] * 0.3, num=9)
            detector = Euclidean()
            detector.trainModel(wolf.getTrainingVector())
            for i in range(10, repeated):
                wolf.setVector(detector.meanVector, num=i)
        animals = AnimalCreator.dict2lst("wolf", wolfStroke)
        animals.update(lambStroke)
        return animals


if __name__ == '__main__':
    unittest.main()
    # for user in  AnimalCreator.create_sheep(3, repeated=2,  size=3).values():
    #     pprint(user.getStrokes())
    # for user in AnimalCreator.create_goat(3, repeated=2,  size=3).values():
    #     pprint(user.getStrokes())
    # for userID,user in AnimalCreator.create_lambs_and_wolves(3, repeated=12,  size=3).items():
    #     print(userID)
    #     pprint(user.getStrokes(12))
