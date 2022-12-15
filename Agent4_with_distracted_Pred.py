from GenerateGraph import GenerateGraph

import random
from UtilityFunctions import Utility
import time
from copy import copy


class Agent4:
    def __init__(self):
        self.generateGraph = GenerateGraph()

    def nextbeliefArray(self, beliefArray, graph, degree, preyPos):
        # def perculateBeliefArray(self, graph, degree):
        nextTimeStepBeliefArray2 = [0 for i in range(len(self.beliefArray))]
        for i in range(len(self.beliefArray)):
            neighbours = Utility.getNeighbours(graph, i)
            neighbours.append(i)
            for neighbor in neighbours:
                nextTimeStepBeliefArray2[i] += self.beliefArray[neighbor] / (
                    degree[neighbor] + 1
                )

        # print("sum after distributing: ", sum(nextTimeStepBelief
        return nextTimeStepBeliefArray2

    def calculateHeuristic(
        self, agentPos, preyPos, predPos, nextPreyPositions, dist, beliefArray, graph
    ):
        agentNeighbours = Utility().getNeighbours(graph, agentPos)

        heuristics = {}
        for n in agentNeighbours:

            currheuristic = 0
            for i in nextPreyPositions:

                neighbourPredDsitance = dist[n][predPos] + 1

                deno = (neighbourPredDsitance + 0.1) ** 10

                currheuristic += (dist[n][i] * (1 - beliefArray[i])) / deno

            heuristics[n] = currheuristic

        return heuristics

    def findNodeToScout(self):
        options = []
        maxiValue = max(self.beliefArray)

        for i, j in enumerate(self.beliefArray):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)

    def updateBeliefArray(self, agentPos, preyPos, predPos, graph, dist, degree):

        nextTimeStepBeliefArray = [0 for i in range(len(self.beliefArray))]

        scoutNode = agentPos

        if scoutNode == preyPos:
            nextTimeStepBeliefArray[scoutNode] = 1
            self.numberOfSuccessfulScouts += 1
        else:
            nextTimeStepBeliefArray[scoutNode] = 0
            for i in range(len(nextTimeStepBeliefArray)):
                if i != scoutNode:
                    nextTimeStepBeliefArray[i] = self.beliefArray[i] / (
                        1 - self.beliefArray[scoutNode]
                    )

            # print("sum before distributing: ", sum(nextTimeStepBeliefArray))
        self.beliefArray = copy(nextTimeStepBeliefArray)

    def NormalizeBeliefArray(self, agentPos, preyPos, predPos, graph, dist, degree):
        nextTimeStepBeliefArray2 = [0 for i in range(len(self.beliefArray))]
        for i in range(len(self.beliefArray)):
            neighbours = Utility.getNeighbours(graph, i)
            neighbours.append(i)
            for neighbor in neighbours:
                nextTimeStepBeliefArray2[i] += self.beliefArray[neighbor] / (
                    degree[neighbor] + 1
                )

        # print("sum after distributing: ", sum(nextTimeStepBeliefArray2))
        self.beliefArray = copy(nextTimeStepBeliefArray2)
        self.updateBeliefArray(agentPos, preyPos, predPos, graph, dist, degree)
        # print("sum after distributing: ", sum(nextTimeStepBeliefArray2))

    def predictPreyPos(self):
        options = []
        maxiValue = max(self.beliefArray)

        for i, j in enumerate(self.beliefArray):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)

    def scoutForPrey(self, node, preyPos):
        return node == preyPos

    def moveAgent(
        self, agentPos, predictedPreyPos, preyPos, predPos, graph, dist, degree
    ):

        agentNeighbours = Utility.getNeighbours(graph, agentPos)

        neighboursPreyDistance = []
        neighboursPredatorDistance = []

        currPreyDist = dist[agentPos][predictedPreyPos]
        currPredDist = dist[agentPos][predPos]

        for index, elem in enumerate(agentNeighbours):
            neighboursPreyDistance.append(dist[elem][predictedPreyPos])
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

    def agent3(
        self,
        graph,
        path,
        dist,
        agentPos,
        preyPos,
        predPos,
        degree,
        runs=100,
        visualize=False,
    ):
        self.updateBeliefArray(agentPos, preyPos, predPos, graph, dist, degree)
        # print(self.beliefArray,"test init")

        self.numberOfSuccessfulScouts = 0
        while runs > 0:

            if visualize:
                # wait for a second
                Utility.visualizeGrid(graph, agentPos, predPos, preyPos)
                # time.sleep(10)

            # print(self.beliefArray,"belief input")
            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos
            scoutnode = self.findNodeToScout()
            self.updateBeliefArray(scoutnode, preyPos, predPos, graph, dist, degree)
            # print(self.beliefArray,"after scout")
            predictedPreyPosition = self.predictPreyPos()

            nextTimeStepBeliefArray = self.nextbeliefArray(
                self.beliefArray, graph, degree, predictedPreyPosition
            )

            print("SUM", sum(nextTimeStepBeliefArray))

            nextPreyPositions = []
            # for i, j in enumerate(nextTimeStepBeliefArray):
            #     if j != 0:
            nextPreyPositions.append(predictedPreyPosition)

            heuristicMap = self.calculateHeuristic(
                agentPos,
                preyPos,
                predPos,
                nextPreyPositions,
                dist,
                nextTimeStepBeliefArray,
                graph,
            )

            # move agent
            agentPos = sorted(heuristicMap.items(), key=lambda x: x[1])[0][0]

            # agentPos = self.moveAgent(
            #     agentPos,
            #     predictedPreyPosition,
            #     preyPos,
            #     predPos,
            #     graph,
            #     dist,
            #     degree,
            # )
            self.NormalizeBeliefArray(agentPos, preyPos, predPos, graph, dist, degree)
            print(
                agentPos, preyPos, predPos, predictedPreyPosition, sum(self.beliefArray)
            )
            # print(self.beliefArray, "after normalize")

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
            predPos = Utility.movePredator(agentPos, predPos, graph, dist)

            runs -= 1

        return False, 5, 100, agentPos, predPos, preyPos

    def executeAgent(self, size):

        graph, path, dist, degree = self.generateGraph.generateGraph(size)

        counter = 0

        stepsCount = 0
        for _ in range(100):

            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)
            while predPos == agentPos:
                predPos = random.randint(0, size - 1)

            self.beliefArray = [1 / (size) for i in range(size)]
            result, line, steps, agentPos, predPos, preyPos = self.agent3(
                graph, path, dist, agentPos, preyPos, predPos, degree, 100, False
            )

            print(result, agentPos, predPos, preyPos)
            counter += result
            stepsCount += steps

        return counter, stepsCount / 100


if __name__ == "__main__":

    agent1 = Agent4()
    counter = 0
    stepsArray = []
    successArray = []
    predCatch = []
    successfulScouts = []
    for _ in range(30):

        result, steps = agent1.executeAgent(50)
        successArray.append(result)
        # counter += result
        stepsArray.append(steps)
        # predCatch.append(catches)
        successfulScouts.append(agent1.numberOfSuccessfulScouts)
        # print(catches)
    print(sum(successArray) / 30)
    # print(predCatch)
    print(successArray)
    print(stepsArray)
    print(successfulScouts)
