from GenerateGraph import GenerateGraph

import random
from UtilityFunctions import Utility
import time
import graph as g


class Agent1:
    def __init__(self):
        self.generateGraph = GenerateGraph()
        self.discount = 0.75
        self.nonterminalReward = -0.001
        self.error = 10 ** (-3)

    def computeUtility(self, agentPos, preyPos, predPos, size=50):

        utility = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

        while True:
            pass

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

        while runs > 0:

            print(agentPos, predPos, preyPos)

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
            predPos = Utility.movePredator_dum(agentPos, predPos, graph, dist)

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
