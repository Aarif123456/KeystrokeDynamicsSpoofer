# KeystrokeDynamicsSpoofer
A keystroke biometric spoofer created to test the strength of the strength of various keystroke dynamic based authentication systems

Authenticator using 4 evaluation algorithms
- Euclidean distance
- normalized Euclidean distance
- Manhattan distance
- scaled Manhattan distance

Spoofer 
- Implemented using genetic algorithm to create keystrokes that similar to the target user
- Try using different population to determine optimal setting for your device
- Try different method of evaluation - see which ones run longer 

Classifier - classify users depending on their behavior
- sheep - most people fit here- they have a lower error rate and higher acceptance rate compared to other groups
- goat - their behavior vary to the point where the system has a hard time recognizing them - they tend to get rejected by their own model
- lamb - they seem to be users that are easy to mimic
- wolf - these people have an easier time pretending to be other users


# reference
# 14 algorithms based on - https://www.cs.cmu.edu/~maxion/pubs/KillourhyMaxion09.pdf
# Awesome guide -# https://appliedmachinelearning.blog/2017/07/26/user-verification-based-on-keystroke-dynamics-python-code/