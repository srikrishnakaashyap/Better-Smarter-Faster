from GenerateGraph import GenerateGraph

import random
from UtilityFunctions import Utility
import time
import graph as g
import math


class Agent1:
    def __init__(self):
        self.generateGraph = GenerateGraph()
        self.discount = 0.75
        self.nonterminalReward = -0.001
        self.error = 10 ** (-3)

    def getUtility(self, utility, currState, action):
        pass

    def valueIteration(self, agentPos, preyPos, predPos, size=50):

        utility = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

        for i in range(size):
            for j in range(size):
                utility[i][j][predPos] = -1
                utility[i][preyPos][j] = 1

        while True:

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
                        agentActions = Utility.getNeighbours(agent)
                        preyActions = Utility.getNeighbours(prey)
                        predActions = Utility.getNeighbours(pred)

                        nextVal = -math.inf
                        for newAgent in agentActions:
                            for newPrey in preyActions:
                                for newPred in predActions:

                                    nextVal = max(
                                        nextVal,
                                        self.getUtility(
                                            utility,
                                            (agent, prey, pred),
                                            (newAgent, newPrey, newPred),
                                        ),
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

        utility = self.valueIteration(agentPos, preyPos, predPos, size)

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
