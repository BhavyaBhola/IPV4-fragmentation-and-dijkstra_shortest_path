import math
import sys
from heapq import heapify, heappop, heappush


class fragmentation():
    def __init__(self, payload, mtu):
        self.payload = payload
        self.mtu = mtu
        self.header = 20

    def packet_gen(self):
        n_packets = math.ceil(
            (self.payload - self.header) / (self.mtu - self.header))
        return n_packets


class graph(fragmentation):
    def __init__(self, vertices):
        super().__init__(payload , mtu)
        self.vertices = vertices
        self.graph = [[0 for i in range(self.vertices)]
                      for j in range(self.vertices)]

    def graph_dict(self):
        graph_dict = {}
        for i in range(self.vertices):
            graph_dict[i] = {}
            for j in range(self.vertices):
                if self.graph[i][j] == 0:
                    continue
                graph_dict[i][j] = self.graph[i][j]

        return graph_dict

    def dijkstra_shortest_path(self, source, destination):
        grph = self.graph_dict()
        inf = sys.maxsize
        node_data = {}

        for i in range(self.vertices):
            node_data[i] = {'cost': inf, 'pred': []}

        node_data[source]['cost'] = 0
        visited_node = []
        temp = source

        for i in range(self.vertices):
            if temp not in visited_node:
                visited_node.append(temp)
                min_heap = []
                for j in grph[temp]:
                    if j not in visited_node:
                        cst = node_data[temp]['cost'] + grph[temp][j]
                        if cst < node_data[j]['cost']:
                            node_data[j]['cost'] = cst
                            node_data[j]['pred'] = node_data[temp]['pred'] + [temp]
                        heappush(min_heap, (node_data[j]['cost'], j))
                if min_heap:
                    temp = heappop(min_heap)[1]
                    heapify(min_heap)
                else:
                    break

        print(f"shortest_distance---->{node_data[destination]['cost']}")
        print(
            f"shortest_path---->{node_data[destination]['pred'] +[destination]}")

    def sending_pkts(self):
        n_pkts = self.packet_gen()

        for i in range(n_pkts):

            flag = input('would you like to change the topology of the graph (y/n) ------> ')
            if flag == "y":
                self.vertices = int(input('enter the number of vertices/nodes in the network -----> '))
                self.graph = [[int(input(f'distance/weight between {q}th and {p}th vertex ------> ')) for p in range(self.vertices)] for q in range(self.vertices)]

                print(f"the graph is ------> {self.graph_dict()}")

            src = int(input(f"source of {i+1} th packet ------> "))
            destination = int(input(f"destination for {i+1} th packet -------> "))
            self.dijkstra_shortest_path(src, destination)


if __name__ == "__main__":

    payload = int(input("enter the size of payload: "))
    mtu = int(input("enter the size of MTU: "))
    n_vrts = int(input("The number of vertices/nodes in the network: "))

    g = graph(n_vrts)
    g.payload = payload
    g.mtu = mtu

    print(f"the number of packets generated ------> {g.packet_gen()}")

    g.graph = [[0,7,12,0,0,0],
               [0,0,2,9,0,0],
               [0,0,0,0,10,0],
               [0,0,0,0,0,1],
               [0,0,0,4,0,5],
               [0,0,0,0,0,0]]
    
    
    #g.graph = [[int(input(f'distance/weight between {j}th and {i}th vertex')) for i in range(n_vrts)] for j in range(n_vrts)]
    print(f"the considered topology is ------> {g.graph_dict()} ")
    
    g.sending_pkts()


