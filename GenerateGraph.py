import math
import random
from UtilityFunctions import Utility


class GenerateGraph:
    def addRandomEdges(self, graph, size, degree):

        for i in range(size):

            if degree[i] == 2:
                deg2List = []
                for j in range(i - 5, i + 6):
                    if (
                        i != j
                        and i != j % size
                        and i != (j + 1) % size
                        and i != (j - 1) % size
                        and degree[j % size] == 2
                    ):
                        deg2List.append(j % size)

                deg2List = list(set(deg2List))
                # print(i,deg2List,"test_deg")
                if len(deg2List) != 0:
                    randomEdgeIndex = random.randint(0, len(deg2List) - 1)
                    randomEdge = deg2List[randomEdgeIndex]
                    # print(i,randomEdgeIndex,randomEdge,"test")
                    degree[i] += 1
                    degree[randomEdge] += 1
                    graph[i][randomEdge] = 1
                    graph[randomEdge][i] = 1

    def generateGraph(self, size):

        degree = [2 for i in range(size)]
        graph = [[0 for i in range(size)] for j in range(size)]

        for i in range(size):
            graph[i % size][(i + 1) % size] = 1
            graph[(i + 1) % size][i % size] = 1
        # print(graph,"before")
        self.addRandomEdges(graph, size, degree)

        # print("--------------graph------------")

        # Utility.printGrid(graph)
        # print(graph,"after")
        # print(degree,"degree")
        path, distance = Utility.floydWarshal(graph, size)
        # print("--------------------path--------------")
        # Utility.printGrid(path)

        # print("PATH", path)

        return graph, path, distance, degree


if __name__ == "__main__":
    g = GenerateGraph()

    graph, path, distance, degree = g.generateGraph(5)

    print(graph)

    print(distance)

    print(degree)
