"""
Notes:

Mk. 1 Uses only my attempts at an Evolutionary NN as well as only implementing NN weights and 
not biases. (I have not learned how to properly implement biases yet.)
 - 08/14/2024



"""




import math, random, sys

"""
Key to Acronyms

S = Straight only lane
R = Right turning only lane
L = Left turning only lane
RS = Right turning and straight lane

NN = Neural Network
"""


cars = {
    "North": {"RS": []},
    "East": {"RS": []},
    "South": {"RS": []},
    "West": {"RS": []}
}

lightSystems = []

populationSize = 20
currentID = 0

class BasicLightSystem:

    def __init__(self, ID = 0, NNWeights = {"North": [random.random(), random.random(), random.random(), random.random()], "East": [random.random(), random.random(), random.random(), random.random()], "South": [random.random(), random.random(), random.random(), random.random()], "West": [random.random(), random.random(), random.random(), random.random()]}):
        self.ID = ID
        self.fitness = 0
        self.carsThrough = 0
        self.NNWeights = NNWeights

    def getFitness(self):
        return self.carsThrough
    
    def getNNChoice(self, cars):
        NorthLight = len(cars["North"]["RS"])*self.NNWeights["North"][0] + len(cars["East"]["RS"])*self.NNWeights["East"][0] + len(cars["South"]["RS"])*self.NNWeights["South"][0] + len(cars["West"]["RS"])*self.NNWeights["West"][0] 
        EastLight = len(cars["North"]["RS"])*self.NNWeights["North"][1] + len(cars["East"]["RS"])*self.NNWeights["East"][1] + len(cars["South"]["RS"])*self.NNWeights["South"][1] + len(cars["West"]["RS"])*self.NNWeights["West"][1]
        SouthLight = len(cars["North"]["RS"])*self.NNWeights["North"][2] + len(cars["East"]["RS"])*self.NNWeights["East"][2] + len(cars["South"]["RS"])*self.NNWeights["South"][2] + len(cars["West"]["RS"])*self.NNWeights["West"][2]
        WestLight = len(cars["North"]["RS"])*self.NNWeights["North"][3] + len(cars["East"]["RS"])*self.NNWeights["East"][3] + len(cars["South"]["RS"])*self.NNWeights["South"][3] + len(cars["West"]["RS"])*self.NNWeights["West"][3]
        
        if NorthLight >= EastLight and EastLight >= SouthLight and SouthLight >= WestLight:
            return "North"
        elif EastLight >= SouthLight and SouthLight >= WestLight:
            return "East"
        elif SouthLight >= WestLight:
            return "South"
        else:
            return "West"
        

def createCar():
    global cars
    direction = random.choice(list(cars.keys()))
    lane = random.choice(list(cars[direction].keys()))

    if lane == "S":
        intention = "Straight"
    if lane == "R":
        intention = "Right"
    if lane == "L":
        intention = "Left"
    if lane == "RS":
        intention = random.choice(["Right", "Straight"])

    cars[direction][lane].append(intention)


def sortByFitness():
    global lightSystems
    while True:
        acc = 0
        for i in range(0, len(lightSystems)):
            if i != 0:
                if lightSystems[i].getFitness() > lightSystems[i-1].getFitness():
                    holder = lightSystems[i-1]
                    lightSystems[i-1] = lightSystems[i]
                    lightSystems[i] = holder
                else:
                    acc += 1
            else:
                acc += 1
        if acc == len(lightSystems):
            return


def cullTheWeak(populationSize):
    global lightSystems
    for i in range(populationSize/10, populationSize):
        del(lightSystems[(populationSize/10) + 1])

def repopulateTheStrong(populationSize):
    global lightSystems, currentID

    #REPOPULATION
    intialParents = lightSystems
    for i in range(populationSize/10, populationSize):
        currentID += 1
        parent1 = random.choice(intialParents)
        parent2 = random.choice(intialParents)
        newNNWeights = {"North": [0, 0, 0, 0], "East": [0, 0, 0, 0], "South": [0, 0, 0, 0], "West": [0, 0, 0, 0]}
        for j in range(0, len(newNNWeights["North"]) - 1):
            if random.randint(1, 2) == 1:
                newNNWeights["North"][j] = parent1["North"][j]
            else:
                newNNWeights["North"][j] = parent1["North"][j]

        for j in range(0, len(newNNWeights["East"]) - 1):
            if random.randint(1, 2) == 1:
                newNNWeights["East"][j] = parent1["East"][j]
            else:
                newNNWeights["East"][j] = parent1["East"][j]

        for j in range(0, len(newNNWeights["South"]) - 1):
            if random.randint(1, 2) == 1:
                newNNWeights["South"][j] = parent1["South"][j]
            else:
                newNNWeights["South"][j] = parent1["South"][j]

        for j in range(0, len(newNNWeights["West"]) - 1):
            if random.randint(1, 2) == 1:
                newNNWeights["West"][j] = parent1["West"][j]
            else:
                newNNWeights["West"][j] = parent1["West"][j]
        lightSystems.append(BasicLightSystem(currentID, newNNWeights))
    
    #MUTATION
    for i in range(populationSize/10, populationSize):
        newNNWeights = lightSystems[i]
        for j in range(0, len(newNNWeights["North"]) - 1):
            if random.randint(1, 1000) == 1:
                newNNWeights["North"][i] = random.random()

        for j in range(0, len(newNNWeights["East"]) - 1):
            if random.randint(1, 1000) == 1:
                newNNWeights["East"][i] = random.random()

        for j in range(0, len(newNNWeights["South"]) - 1):
            if random.randint(1, 1000) == 1:
                newNNWeights["South"][i] = random.random()
                
        for j in range(0, len(newNNWeights["West"]) - 1):
            if random.randint(1, 1000) == 1:
                newNNWeights["West"][i] = random.random()



tickNum = 0