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

    def valueIteration(
        self, graph, dist, degree, agentPos, preyPos, predPos, size=50, iterations=100
    ):

        utility = [
            [[-1 for i in range(size)] for j in range(size)] for k in range(size)
        ]

        for i in range(size):
            for j in range(size):
                for k in range(size):

                    # if i == j:
                    utility[i][j][k] = dist[i][j]
                    utility[i][i][j] = 0
                    utility[i][j][i] = math.inf
                    predNeighbours = Utility.getNeighbours(graph, k)
                    for l in predNeighbours:
                        utility[l][j][k] = math.inf

        print(utility)

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
                        nextVal = math.inf
                        # Compute the utility for all the actions
                        agentActions = Utility.getNeighbours(graph, agent)
                        su = 0
                        for newAgent in agentActions:
                            preyActions = Utility.getNeighbours(
                                graph, prey, include=True
                            )
                            predActions = Utility.getNeighbours(graph, pred)

                            s = 0
                            for k in preyActions:
                                for l in predActions:

                                    s += (
                                        self.getProbability(
                                            graph,
                                            dist,
                                            degree,
                                            utility,
                                            (agent, prey, pred),
                                            (newAgent, k, l),
                                        )
                                        * utility[newAgent][k][l]
                                    )

                            nextVal = min(nextVal, s * self.discount)


                        if agent == pred:
                            reward = math.inf
                        elif agent == prey:
                            reward = 0
                        else:
                            reward = 1

                        nextUtility[agent][prey][pred] = reward + nextVal
                        if utility[agent][prey][pred] == math.inf or nextUtility[agent][prey][pred] == math.inf:
                            continue
                        error = max(
                            error,
                            abs(
                                utility[agent][prey][pred]
                                - nextUtility[agent][prey][pred]
                            ),
                        )
            utility = copy.deepcopy(nextUtility)
            print(
                "Value iteration for",
                a,
                error,
                self.error * (1 - self.discount) / self.discount,
                utility
            )
            if error < 10**-15:
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

            maxValue = math.inf
            maxNeighbour = 1

            for n in agentNeighbours:

                val = self.utility[n][preyPos][predPos]

                if val < maxValue:
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
