class Node:
    def __init__(self, id: str):
        self.id: str = id
        self.neighbors: set[Node] = set()
    def add_neighbor(self, neighbor: 'Node'):
        if neighbor in self.neighbors: return
        self.neighbors.add(Node)
        neighbor.add_neighbor(self)
    
    def pos_to_str(pos: list[int]):
        return f'{str(pos[0])}_{str(pos[1])}'

class Net:
    def __init__(self):
        self.nodes: dict[Node] = dict()
        self.links: set[tuple[Node, Node]] = set()
    def add_link(self, node1: list[int], node2: list[int]):
        n1 = self.add_node(node1)
        n2 = self.add_node(node2)
        n1.add_neightbor(n2)
    def add_node(self, pos: list[int]):
        n = Node.pos_to_str(pos)
        self.nodes[n] = Node(n)
        return n
    


class Solution:
    def removeStones(self, stones: list[list[int]]) -> int:
        pass