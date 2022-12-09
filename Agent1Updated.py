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
        self.error = 10 ** (-3)

    def getUtility(self, graph, dist, utility, currState, action):
        u = self.nonterminalReward
        preyVal = 0
        predVal = float("-inf")
        agentVal = utility[action[0]][action[1]][action[2]]
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
        return u + agentVal + preyVal + predVal

    def valueIteration(self, graph, dist, agentPos, preyPos, predPos, size=50):

        utility = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

        for i in range(size):
            for j in range(size):
                utility[i][preyPos][j] = 1
                utility[i][j][predPos] = -1

        # return utility

        # print(utility)
        a = 0
        while True:

            a += 1
            error = 0

            nextUtility = [
                [[0 for i in range(size)] for j in range(size)] for k in range(size)
            ]
            for i in range(size):
                for j in range(size):
                    nextUtility[i][j][predPos] = -1
                    nextUtility[i][preyPos][j] = 1

            # Compute Next Utility

            # For all the states
            for agent in range(size):
                for prey in range(size):
                    for pred in range(size):

                        # Compute the utility for all the actions
                        agentActions = Utility.getNeighbours(graph, agent)
                        preyActions = Utility.getNeighbours(graph, prey)
                        predActions = Utility.getNeighbours(graph, pred)

                        nextVal = -math.inf
                        for newAgent in agentActions:
                            for newPrey in preyActions:
                                for newPred in predActions:

                                    nextVal = max(
                                        nextVal,
                                        self.getUtility(
                                            graph,
                                            dist,
                                            utility,
                                            (agent, prey, pred),
                                            (newAgent, newPrey, newPred),
                                        )
                                        * self.discount,
                                    )

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

    def preyUtility(self, graph, dist, utility, currState, action):
        pass

    def predUtility(self, graph, dist, utility, currState, action):
        pass

    def preyValueIteration(self, graph, dist, agentPos, preyPos, predPos, size):
        pass

    def predValueIteration(self, graph, dist, agentPos, preyPos, predPos, size):
        pass

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

        print(utility)
        return False, 5, 100, agentPos, predPos, preyPos

    def executeAgent(self, size):

        # graph, path, dist, degree = self.generateGraph.generateGraph(size)

        graph, dist, degree = g.getGraph()

        counter = 0

        stepsCount = 0
        for _ in range(1):

            agentPos = 1
            preyPos = 7
            predPos = 4

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

        result, steps = agent1.executeAgent(10)
        counter += result
        stepsArray.append(steps)
    print(counter, stepsArray)
