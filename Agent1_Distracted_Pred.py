from GenerateGraph import GenerateGraph
import random
from UtilityFunctions import Utility
import time


class Agent1:
    def __init__(self):
        self.generateGraph = GenerateGraph()

    def moveAgent(self, agentPos, preyPos, predPos, graph, dist):

        agentNeighbours = Utility.getNeighbours(graph, agentPos)

        neighboursPreyDistance = []
        neighboursPredatorDistance = []

        currPreyDist = dist[agentPos][preyPos]
        currPredDist = dist[agentPos][predPos]

        for index, elem in enumerate(agentNeighbours):
            neighboursPreyDistance.append(dist[elem][preyPos])
            neighboursPredatorDistance.append(dist[elem][predPos])

        options = []
        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] < currPreyDist
                and neighboursPredatorDistance[i] > currPredDist
            ):
                options.append(agentNeighbours[i])

        # Break ties by choosing optimal choice for agent 2
        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] < currPreyDist
                and neighboursPredatorDistance[i] == currPredDist
            ):
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] == currPreyDist
                and neighboursPredatorDistance[i] > currPredDist
            ):
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] == currPreyDist
                and neighboursPredatorDistance[i] == currPredDist
            ):
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if neighboursPredatorDistance[i] > currPredDist:
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if neighboursPredatorDistance[i] == currPredDist:
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        return agentPos

    def agent1(
        self, graph, path, dist, agentPos, preyPos, predPos, runs=100, visualize=False
    ):

        while runs > 0:

            # print(agentPos, predPos, preyPos)

            if visualize:
                # wait for a second
                Utility.visualizeGrid(graph, agentPos, predPos, preyPos)
                # time.sleep(10)

            # print(agentPos, preyPos, predPos)
            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos

            # move agent
            agentPos = self.moveAgent(agentPos, preyPos, predPos, graph, dist)

            # check pred
            if agentPos == predPos:
                return False, 4, 100 - runs, agentPos, predPos, preyPos

            # check prey
            if agentPos == preyPos:
                return True, 1, 100 - runs, agentPos, predPos, preyPos

            # move prey
            preyPos = Utility.movePrey(preyPos, graph)

            if agentPos == preyPos:
                return True, 2, 100 - runs, agentPos, predPos, preyPos

            # move predator
            # predPos = Utility.movePredator(agentPos, predPos, path)
            predPos = Utility.movePredator(agentPos, predPos, graph, dist)

            runs -= 1

        return False, 5, 100, agentPos, predPos, preyPos

    def executeAgent(self, size):

        graph, path, dist, degree = self.generateGraph.generateGraph(size)

        counter = 0

        stepsCount = 0

        predCatch = 0
        for _ in range(100):

            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)
            while predPos == agentPos:
                predPos = random.randint(0, size - 1)
            result, line, steps, agentPos, predPos, preyPos = self.agent1(
                graph, path, dist, agentPos, preyPos, predPos, 100, False
            )

            # print(result, agentPos, predPos, preyPos)
            counter += result
            stepsCount += steps

            if not result:
                predCatch += 1
        # print(self.agent1(graph, path, dist, agentPos, preyPos, predPos))
        # print(result, line)

        return counter, stepsCount / 100, predCatch


if __name__ == "__main__":

    agent1 = Agent1()
    counter = 0
    stepsArray = []
    successArray = []
    predCatch = []
    for _ in range(30):

        result, steps, catches = agent1.executeAgent(50)
        successArray.append(result)
        # counter += result
        stepsArray.append(steps)
        predCatch.append(catches)
        # print(catches)
    print(sum(successArray)/30)
    print(predCatch)
    print(successArray)
    print(stepsArray)
