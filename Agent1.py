from GenerateGraph import GenerateGraph
from collections import defaultdict
import random
from UtilityFunctions import Utility
import time
import graph as g
import math
import copy
import json


class Agent1:
    def __init__(self):
        self.generateGraph = GenerateGraph()
        self.discount = 0.75
        self.nonterminalReward = -0.001
        self.error = 1e-22

        self.utility = None

    def getUtility(self, graph, dist, utility, currState, action):
        u = self.nonterminalReward
        neighbours = Utility.getNeighbours(graph, action[2])
        neighbourDistanceMap = defaultdict(list)
        for n in neighbours:
            neighbourDistanceMap[dist[n][action[0]]].append(n)
        minimumDistanceList = neighbourDistanceMap.get(min(neighbourDistanceMap), [])
        preyVal = 0
        predVal = float("-inf")
        agentVal = utility[action[0]][action[1]][action[2]]
        agentNeighbours = Utility.getNeighbours(graph, action[0])
        preyNeighbours = Utility.getNeighbours(graph, action[1])
        for n in preyNeighbours:
            preyVal += utility[action[0]][n][action[2]] / len(preyNeighbours)
        currPredNeighbours = Utility.getNeighbours(graph, currState[2])
        for i in currPredNeighbours:
            tempVal = 0.6 * utility[action[0]][action[1]][i]
            for j in currPredNeighbours:
                if i != j:
                    tempVal += (
                        utility[action[0]][action[1]][j]
                        * 0.4
                        / (len(currPredNeighbours) - 1)
                    )
            predVal = max(predVal, tempVal)
        return (u + agentVal) * (u + preyVal) * (u + predVal)

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
        return agentProbability * preyProbability * predProbability

    def valueIteration(
        self, graph, dist, degree, agentPos, preyPos, predPos, size=50, iterations=100
    ):

        utility = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

        for i in range(size):
            for j in range(size):
                # if i == j:
                utility[i][i][j] = 1
                utility[i][j][i] = -1
        a = 0
        while iterations > 0:

            a += 1
            error = 0

            nextUtility = copy.deepcopy(utility)

            # Compute Next Utility

            # For all the states
            for agent in range(size):
                for prey in range(size):
                    for pred in range(size):

                        # For all the actions

                        # Compute the utility for all the actions
                        agentActions = Utility.getNeighbours(graph, agent)
                        preyActions = Utility.getNeighbours(graph, prey)
                        predActions = Utility.getNeighbours(graph, pred)

                        nextVal = -math.inf

                        for newAgent in agentActions:
                            for newPrey in preyActions:
                                for newPred in predActions:

                                    if newAgent == newPred:
                                        reward = -1
                                    elif newAgent == newPrey:
                                        reward = 1
                                    else:
                                        reward = 0

                                    nextVal = max(nextVal, reward+ self.getProbability(
                                                graph,
                                                dist,
                                                degree,
                                                utility,
                                                (agent, prey, pred),
                                                (newAgent, newPrey, newPred))*( utility[newAgent][newPrey][newPred]* self.discount))
                        if abs(utility[agent][prey][pred]- nextUtility[agent][prey][pred])>self.discount:
                            self.discount = abs(utility[agent][prey][pred]- nextUtility[agent][prey][pred])

                        nextUtility[agent][prey][pred] =  max(nextVal, abs(utility[agent][prey][pred]- nextUtility[agent][prey][pred]))
                        error = max(
                            error,
                            abs(
                                utility[agent][prey][pred]
                                - nextUtility[agent][prey][pred]
                            ),
                        )

            utility = nextUtility
            print(
                "Value iteration for",
                a,
                error,
                self.error * (1 - self.discount) / self.discount,
            )
            if error < self.error * (1 - self.discount) / self.discount:
                break

            iterations -= 1

        return utility

    def agent1(
        self,
        graph,
        dist,
        degree,
        agentPos,
        preyPos,
        predPos,
        size=50,
        runs=100,
        visualize=False,
    ):

        if self.utility is None:

            self.utility = self.valueIteration(
                graph, dist, degree, agentPos, preyPos, predPos, size
            )

            with open("test.txt", "w") as f:

                f.write(json.dumps(self.utility))

            print(self.utility)

        while runs > 0:

            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos

            agentNeighbours = Utility.getNeighbours(graph, agentPos)

            maxValue = -math.inf
            maxNeighbour = -1

            for n in agentNeighbours:

                val = self.utility[n][preyPos][predPos]

                if val > maxValue:
                    maxValue = val
                    maxNeighbour = n

            agentPos = maxNeighbour

            if agentPos == predPos:
                return False, 4, 100 - runs, agentPos, predPos, preyPos

            # check prey
            if agentPos == preyPos:
                return True, 1, 100 - runs, agentPos, predPos, preyPos

            preyPos = Utility.movePrey(preyPos, graph)

            if agentPos == preyPos:
                return True, 2, 100 - runs, agentPos, predPos, preyPos

            predPos = Utility.movePredator(agentPos, predPos, graph, dist)

            runs -= 1

        return False, 5, 100, agentPos, predPos, preyPos

    def executeAgent(self, size):

        # graph, path, dist, degree = self.generateGraph.generateGraph(size)

        graph, dist, degree = (
            g.getGraph(),
            g.getDist(),
            g.getDegree(),
        )
        counter = 0

        stepsCount = 0
        for _ in range(100):

            agentPos = random.randint(0, 49)
            preyPos = random.randint(0, 49)
            predPos = random.randint(0, 49)

            result, line, steps, agentPos, predPos, preyPos = self.agent1(
                graph, dist, degree, agentPos, preyPos, predPos, size, 100, False
            )

            print(result, agentPos, predPos, preyPos)
            counter += result
            stepsCount += steps
        # print(self.agent1(graph, path, dist, agentPos, preyPos, predPos))
        # print(result, line)

        return counter, stepsCount / 100


if __name__ == "__main__":

    agent1 = Agent1()
    counter = 0
    stepsArray = []
    for _ in range(1):

        result, steps = agent1.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    print(counter, stepsArray)
