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
        self.discount = 0.95
        self.nonterminalReward = -0.1
        self.error = 1e-30

        self.utility = None

    def getProbability(self, graph, dist, degree, utility, currState, nextState):
        agentProbability = 1
        preyProbability = 1 / (degree[currState[1]] + 1)
        predNeighbours = Utility.getNeighbours(graph, currState[2])
        neighbourDistanceMap = defaultdict(list)
        for n in predNeighbours:
            neighbourDistanceMap[dist[n][nextState[0]]].append(n)
        minimumDistanceList = neighbourDistanceMap.get(min(neighbourDistanceMap), [])
        if nextState[2] in minimumDistanceList:
            predProbability = 0.6 / (len(minimumDistanceList)) + 0.4 / (
                degree[currState[2]]
            )
        else:
            predProbability = 0.4 / (degree[currState[2]])
        return agentProbability * preyProbability * predProbability

    def valueIteration(
        self, graph, dist, degree, agentPos, preyPos, predPos, size=50, iterations=100
    ):

        utility = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

        for i in range(size):
            for j in range(size):
                for k in range(size):
                    # # if i == j:
                    utility[i][j][k] = 1 / (1 + dist[i][j])
                    utility[i][i][j] = 1
                    utility[i][j][i] = -1
        a = 0
        while iterations > 0:

            a += 1
            error = 0

            # nextUtility = [
            #     [[0 for i in range(size)] for j in range(size)] for k in range(size)
            # ]

            # for i in range(size):
            #     for j in range(size):
            #         for k in range(size):
            #             # # if i == j:
            #             # utility[i][j][k] = 1 / (1 + dist[i][j])
            #             nextUtility[i][i][k] = 1
            #             nextUtility[k][j][k] = -1

            nextUtility = copy.deepcopy(utility)

            # Compute Next Utility

            # For all the states
            for agent in range(size):
                for prey in range(size):
                    for pred in range(size):

                        # if agent == prey or agent == pred:
                        #     continue

                        # For all the actions

                        # Compute the utility for all the actions
                        agentActions = [0, 1]
                        pre
                        agentActions = Utility.getNeighbours(graph, agent)
                        preyActions = Utility.getNeighbours(graph, prey, include=True)
                        predActions = Utility.getNeighbours(graph, pred)

                        nextVal = -math.inf

                        # Actions

                        for newAgent in agentActions:
                            for newPrey in preyActions:
                                for newPred in predActions:

                                    nextVal = max(
                                        nextVal,
                                        (
                                            self.getProbability(
                                                graph,
                                                dist,
                                                degree,
                                                utility,
                                                (agent, prey, pred),
                                                (newAgent, newPrey, newPred),
                                            )
                                            * utility[newAgent][newPrey][newPred]
                                        ),
                                    )

                        if pred == agent:
                            reward = -1
                        elif prey == agent:
                            reward = 1
                        else:
                            reward = self.nonterminalReward

                        nextUtility[agent][prey][pred] = reward + (
                            self.discount * nextVal
                        )
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
            )
            if error < self.error * (1 - self.discount) / self.discount:
                break

            iterations -= 1

        return utility

    def getOptimalPolicy(self, utility, graph, dist, degree):
        size = len(utility)
        policy = [[[0 for i in range(size)] for j in range(size)] for k in range(size)]

        for agent in range(size):
            for prey in range(size):
                for pred in range(size):

                    maxAction = None
                    maxUtility = -1

                    agentActions = Utility.getNeighbours(graph, agent)
                    preyActions = Utility.getNeighbours(graph, prey, include=True)
                    predActions = Utility.getNeighbours(graph, pred)

                    for newAgent in agentActions:
                        for newPrey in preyActions:
                            for newPred in predActions:
                                v = (
                                    self.getProbability(
                                        graph,
                                        dist,
                                        degree,
                                        utility,
                                        (agent, prey, pred),
                                        (newAgent, newPrey, newPred),
                                    )
                                    * utility[newAgent][newPrey][newPred]
                                )

                                reward = 0
                                if newPred == newAgent:
                                    reward = -1
                                elif newPrey == newAgent:
                                    reward = 1
                                else:
                                    reward = self.nonterminalReward

                                u = reward + (self.discount * v)

                                if u > maxUtility:
                                    maxUtility, maxAction = u, newAgent

                    policy[agent][prey][pred] = maxAction

        return policy

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

            # print(self.utility)

        # policy = self.getOptimalPolicy(self.utility, graph, dist, degree)

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

        graph, dist, degree = g.getGraph()
        counter = 0

        stepsCount = 0
        for _ in range(100):

            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)

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

        result, steps = agent1.executeAgent(5)
        counter += result
        stepsArray.append(steps)
    print(counter, stepsArray)
