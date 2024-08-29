class Node:
    def __init__(self, id: str):
        self.id: str = id
        self.neighbors: list[Node] = list()
    def __repr__(self) -> str:
        return f'Node({self.id})'
    def add_neighbor(self, neighbor: 'Node'):
        if neighbor in self.neighbors: return
        self.neighbors.append(neighbor)
        neighbor.add_neighbor(self)
    def remove_neighbor(self, neighbor: 'Node'):
        if neighbor not in self.neighbors: return
        self.neighbors.remove(neighbor)
        neighbor.remove_neighbor(self)
    def degree(self) -> int:
        return len(self.neighbors)
    def neighborhood(self) -> list[str]:
        return [n.id for n in self.neighbors]
    @staticmethod
    def pos_to_str(pos: list[int]) -> str:
        return f'{str(pos[0])}_{str(pos[1])}'
    @staticmethod
    def str_to_pos(string: str) -> list[int]:
        return [int(s) for s in string.split('_')]

class Net:
    def __init__(self):
        self.nodes: dict[str, Node] = dict()
    def add_link(self, node1: list[int], node2: list[int]):
        n1 = self.add_node(node1)
        n2 = self.add_node(node2)
        n1.add_neighbor(n2)
    def add_node(self, pos: list[int]) -> Node:
        n = Node.pos_to_str(pos)
        if n not in self.nodes:
            self.nodes[n] = Node(n)
        return self.nodes[n]
    def has_links(self) -> bool:
        for n in self.nodes.values():
            if n.degree() > 0:
                return True
        return False
    def delete_nodes(self, nodes: list[Node]):
        for node in nodes:
            if node.id in self.nodes:
                self.nodes.pop(node.id)
            for neighbor in list(node.neighbors):
                node.remove_neighbor(neighbor)
    def lowest_degree_node(self) -> Node | None:
        min_node: Node | None = None
        for node in self.nodes.values():
            if node.degree() == 0:
                continue
            if min_node is None:
                min_node = node
                continue
            if min_node.degree() == 1:
                break
            if node.degree() < min_node.degree():
                min_node = node
        return min_node
    @staticmethod
    def travel_from(node: Node, path:list[Node]=[]) -> list[Node]:
        if node in path: return path

        path.append(node)

        if node.degree == 0: return path

        for next_node in node.neighbors:
            if next_node in path: continue
            Net.travel_from(next_node, path=path)

        return path
    def prune_all_paths(self) -> int:
        total_removed: int = 0
        while True:
            lowest = self.lowest_degree_node()
            if lowest is None or not self.has_links(): break
            path = Net.travel_from(lowest, [])
            total_removed += len(path) - 1
            self.delete_nodes(path[1:])
        return total_removed

class Solution:
    @staticmethod
    def get_stones_set(stones: list[list[int]]) -> dict[str, list[int]]:
        return {Node.pos_to_str(s): s for s in stones}
    @staticmethod
    def get_max(stones: list[list[int]]) -> tuple[int, int]:
        mx = 0
        my = 0
        for stone in stones:
            if stone[0] > mx: mx = stone[0]
            if stone[1] > my: my = stone[1]
        return mx, my
    def removeStones(self, stones: list[list[int]]) -> int:
        net = Net()
        mx, my = Solution.get_max(stones)
        sorted_stones = sorted(stones, key=lambda x:x[1])
        sorted_stones = sorted(sorted_stones, key=lambda x:x[0])
        print(sorted_stones)
        for i, stone in enumerate(sorted_stones):
            if i == len(sorted_stones) - 1: break
            next_stone = sorted_stones[i + 1]
            if next_stone[0] != stone[0]: continue
            net.add_link(stone, next_stone)
        sorted_stones = sorted(sorted_stones, key=lambda x:x[1])
        for i, stone in enumerate(sorted_stones):
            if i == len(sorted_stones) - 1: break
            next_stone = sorted_stones[i + 1]
            if next_stone[1] != stone[1]: continue
            net.add_link(stone, next_stone)
        return net.prune_all_paths()

if __name__=='__main__':
    solution = Solution()
    print(solution.removeStones([[3,2],[3,1],[4,4],[1,1],[0,2],[4,0]]))