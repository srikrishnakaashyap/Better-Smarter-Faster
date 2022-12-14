from GenerateGraph import GenerateGraph
from collections import defaultdict
import random
from UtilityFunctions import Utility
import csv
import graph as g
import math
import copy
import json
from numpy import Inf


class Agent1:
    def __init__(self):
        self.generateGraph = GenerateGraph()
        self.discount = 0.75
        self.nonterminalReward = -0.001
        self.error = 1e-15

        self.utility = None

    def moveAgent1(self, agentPos, preyPos, predPos, graph, dist):

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

    def nextbeliefArray(self, beliefArray, graph, degree, preyPos):
        # def perculateBeliefArray(self, graph, degree):
        nextTimeStepBeliefArray2 = [0 for i in range(len(beliefArray))]
        for i in range(len(beliefArray)):
            neighbours = Utility.getNeighbours(graph, i)
            neighbours.append(i)
            for neighbor in neighbours:
                nextTimeStepBeliefArray2[i] += beliefArray[neighbor] / (
                    degree[neighbor] + 1
                )

        # print("sum after distributing: ", sum(nextTimeStepBelief
        return nextTimeStepBeliefArray2

    def calculateHeuristic(
        self, agentPos, preyPos, predPos, nextPreyPositions, dist, beliefArray, graph
    ):
        agentNeighbours = Utility().getNeighbours(graph, agentPos)
        agentNeighbours.append(agentPos)

        heuristics = {}
        for n in agentNeighbours:

            currheuristic = 0
            for i in nextPreyPositions:

                neighbourPredDsitance = dist[n][predPos] + 1

                deno = (neighbourPredDsitance + 0.1) ** 10

                currheuristic += dist[n][i] * (1 - beliefArray[i]) / deno

            heuristics[n] = currheuristic

        return heuristics

    def getUtilityFromFile(self):
        utility = [[[-1 for i in range(50)] for j in range(50)] for k in range(50)]
        with open("data.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    utility[int(row[0])][int(row[1])][int(row[2])] = float(row[-1])
                    line_count += 1
        return utility

    def getProbability(self, graph, dist, degree, utility, currState, nextState):
        """
        Adding rewards for taking that particular action
        """
        agentProbability = 1
        preyProbability = 1 / (degree[currState[1]] + 1)

        predNeighbours = Utility.getNeighbours(graph, currState[2])

        neighbourDistanceMap = defaultdict(list)
        for n in predNeighbours:
            neighbourDistanceMap[dist[n][nextState[0]]].append(n)
        minimumDistanceList = neighbourDistanceMap.get(min(neighbourDistanceMap), [])
        if nextState[2] in minimumDistanceList:
            predProbability = 0.6 / (len(minimumDistanceList)) + 0.4 / (
                degree[currState[2]] + 1
            )
        else:
            predProbability = 0.4 / (degree[currState[2]] + 1)
        # print(preyProbability, predProbability,"test")
        return preyProbability * predProbability

    def agent1(
        self,
        graph,
        dist,
        degree,
        agent1Pos,
        agent2Pos,
        agentUPos,
        preyPos,
        pred1Pos,
        pred2Pos,
        predUPos,
        size=50,
        runs=100,
        visualize=False,
    ):

        if self.utility is None:
            self.utility = self.getUtilityFromFile()

        agent1Break = False
        agent2Break = False
        agentUBreak = False
        agent1Path = []
        agent2Path = []
        agentUPath = []
        preyPath = []
        pred1Path = []
        pred2Path = []
        predUPath = []
        while runs > 0:

            if agent1Break and agent2Break and agentUBreak:
                return (
                    agent1Path,
                    agent2Path,
                    agentUPath,
                    preyPath,
                    pred1Path,
                    pred2Path,
                    predUPath,
                )

            agent1Path.append(agent1Pos)
            agent2Path.append(agent2Pos)
            agentUPath.append(agentUPos)
            preyPath.append(preyPos)
            pred1Path.append(pred1Pos)
            pred2Path.append(pred2Pos)
            predUPath.append(predUPos)

            if agent1Pos == pred1Pos:
                agent1Break = True

            if agent1Pos == preyPos:
                agent1Break = True

            if agent2Pos == pred2Pos:
                agent1Break = True

            if agent2Pos == preyPos:
                agent1Break = True

            if agentUPos == predUPos:
                agent1Break = True

            if agentUPos == preyPos:
                agent1Break = True

            agentUNeighbours = Utility.getNeighbours(graph, agentUPos)

            maxValue = math.inf
            maxNeighbour = 1

            for n in agentUNeighbours:

                val = self.utility[n][preyPos][predUPos]

                if val < maxValue:
                    maxValue = val
                    maxNeighbour = n

            # Move agent U
            agentUPos = maxNeighbour

            # Move Agent 1
            agent1Pos = self.moveAgent1(agent1Pos, preyPos, pred1Pos, graph, dist)

            # Move Agent 2
            beliefArray = [0 for i in range(len(graph))]

            beliefArray[preyPos] = 1

            nextTimeStepBeliefArray = self.nextbeliefArray(
                beliefArray, graph, degree, preyPos
            )

            nextPreyPositions = []
            for i, j in enumerate(nextTimeStepBeliefArray):
                if j != 0:
                    nextPreyPositions.append(i)

            heuristicMap = self.calculateHeuristic(
                agent2Pos,
                preyPos,
                pred2Pos,
                nextPreyPositions,
                dist,
                nextTimeStepBeliefArray,
                graph,
            )

            # move agent
            agent2Pos = sorted(heuristicMap.items(), key=lambda x: x[1])[0][0]

            if agent1Pos == pred1Pos:
                agent1Break = True

            if agent1Pos == preyPos:
                agent1Break = True

            if agent2Pos == pred2Pos:
                agent1Break = True

            if agent2Pos == preyPos:
                agent1Break = True

            if agentUPos == predUPos:
                agent1Break = True

            if agentUPos == preyPos:
                agent1Break = True

            preyPos = Utility.movePrey(preyPos, graph)

            if agent1Pos == preyPos:
                agent1Break = True

            if agent2Pos == preyPos:
                agent2Break = True

            if agentUPos == preyPos:
                agentUBreak = True

            pred1Pos = Utility.movePredator(agent1Pos, pred1Pos, graph, dist)
            pred2Pos = Utility.movePredator(agent1Pos, pred2Pos, graph, dist)
            predUPos = Utility.movePredator(agent1Pos, predUPos, graph, dist)

            runs -= 1
        return (
            agent1Path,
            agent2Path,
            agentUPath,
            preyPath,
            pred1Path,
            pred2Path,
            predUPath,
        )

    def executeAgent(self, size):

        # graph, path, dist, degree = self.generateGraph.generateGraph(size)

        graph, dist, degree = (
            g.getGraph(),
            g.getDist(),
            g.getDegree(),
        )
        counter = 0

        (
            agent1Path,
            agent2Path,
            agentUPath,
            preyPath,
            pred1Path,
            pred2Path,
            predUPath,
        ) = (
            -1,
            -1,
            -1,
            -1,
            -1,
            -1,
            -1,
        )

        stepsCount = 0
        for _ in range(1):

            agent1Pos = random.randint(0, size - 1)
            agent2Pos = agent1Pos
            agentUPos = agent1Pos
            preyPos = random.randint(0, size - 1)

            pred1Pos = random.randint(0, size - 1)
            while pred1Pos == agent1Pos:
                pred1Pos = random.randint(0, size - 1)

            pred2Pos = random.randint(0, size - 1)
            while pred2Pos == agent2Pos:
                pred2Pos = random.randint(0, size - 1)

            predUPos = random.randint(0, size - 1)
            while predUPos == agentUPos:
                predUPos = random.randint(0, size - 1)

            (
                agent1Path,
                agent2Path,
                agentUPath,
                preyPath,
                pred1Path,
                pred2Path,
                predUPath,
            ) = self.agent1(
                graph,
                dist,
                degree,
                agent1Pos,
                agent2Pos,
                agentUPos,
                preyPos,
                pred1Pos,
                pred2Pos,
                predUPos,
                size,
                100,
                False,
            )

        print("AGENT 1 Path", agent1Path)
        print("AGENT 2 Path", agent2Path)
        print("AGENT U Path", agentUPath)
        print("Prey Path", preyPath)
        print("Pred 1 Path", pred1Path)
        print("Pred 2 Path", pred2Path)
        print("Pred U Path", predUPath)

        return (
            agent1Path,
            agent2Path,
            agentUPath,
            preyPath,
            pred1Path,
            pred2Path,
            predUPath,
        )


if __name__ == "__main__":

    agent1 = Agent1()
    counter = 0
    stepsArray = []

    (
        agent1Path,
        agent2Path,
        agentUPath,
        preyPath,
        pred1Path,
        pred2Path,
        predUPath,
    ) = agent1.executeAgent(50)

    print(counter, stepsArray)
