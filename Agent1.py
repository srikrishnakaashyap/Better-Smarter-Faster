from GenerateGraph import GenerateGraph

import random
from UtilityFunctions import Utility
import time
import graph as g
import math
import copy


class Agent1:
    def __init__(self):
        self.generateGraph = GenerateGraph()
        self.discount = 0.75
        self.nonterminalReward = -0.001
        self.error = 1e-22

    def getUtility(self, graph, dist, utility, currState, action):
        u = self.nonterminalReward
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

    def getProbability(self, graph, dist, utility, currState, action):
        pass

    def valueIteration(self, graph, dist, agentPos, preyPos, predPos, size=50):

        utility = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

        for i in range(size):
            for j in range(size):
                utility[i][j][predPos] = -1
                utility[i][preyPos][j] = 1
        a = 0
        while True:

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
                        for preyaction in preyActions:
                            optimalagentdist = float("inf")
                            optimalAgentAction = None
                            for agentaction in agentActions:
                                if dist[agentaction][preyaction] < optimalagentdist:
                                    optimalagentdist = dist[agentaction][preyaction]
                                    optimalAgentAction = agentaction
                            optimalpreddist = float("inf")
                            optimalPredAction = None
                            for predaction in predActions:
                                if dist[agentaction][predaction] < optimalpreddist:
                                    optimalpreddist = dist[agentaction][predaction]
                                    optimalPredAction = predaction

                        nextVal = -math.inf

                        nextUtility[agent][prey][pred] = nextVal
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

        return utility

    def agent1(
        self,
        graph,
        dist,
        agentPos,
        preyPos,
        predPos,
        size=50,
        runs=100,
        visualize=False,
    ):

        utility = self.valueIteration(graph, dist, agentPos, preyPos, predPos, size)
        # while runs > 0:

        #     if agentPos == predPos:
        #         return False, 3, 100 - runs, agentPos, predPos, preyPos

        #     if agentPos == preyPos:
        #         return True, 0, 100 - runs, agentPos, predPos, preyPos

        #     agentNeighbours = Utility.getNeighbours(agentPos)

        #     maxValue = -math.inf
        #     maxNeighbour = -1

        #     for n in agentNeighbours:

        #         val = utility[n][preyPos][predPos]

        #         if val > maxValue:
        #             maxVale = val
        #             maxNeighbour = n

        #     agentPos = maxNeighbour

        #     if agentPos == predPos:
        #         return False, 4, 100 - runs, agentPos, predPos, preyPos

        #     # check prey
        #     if agentPos == preyPos:
        #         return True, 1, 100 - runs, agentPos, predPos, preyPos

        #     preyPos = Utility.movePrey(preyPos, graph)

        #     if agentPos == preyPos:
        #         return True, 2, 100 - runs, agentPos, predPos, preyPos

        #     predPos = Utility.movePredator(agentPos, predPos, graph, dist)

        #     runs -= 1

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
        for _ in range(1):

            agentPos = 1
            preyPos = 28
            predPos = 37

            result, line, steps, agentPos, predPos, preyPos = self.agent1(
                graph, dist, agentPos, preyPos, predPos, size, 100, False
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
