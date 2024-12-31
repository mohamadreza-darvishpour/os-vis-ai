import sys
from typing import List

class GraphColoringIDS:
    def __init__(self, adjacency_matrix: List[List[int]], num_colors: int):
        self.adjacency_matrix = adjacency_matrix
        self.num_colors = num_colors
        self.num_nodes = len(adjacency_matrix)
        self.colors = [-1] * self.num_nodes

    def is_valid_color(self, node: int, color: int) -> bool:
        """Check if assigning `color` to `node` is valid."""
        for neighbor in range(self.num_nodes):
            if self.adjacency_matrix[node][neighbor] == 1 and self.colors[neighbor] == color:
                return False
        return True

    def ids_coloring(self) -> List[int]:
        """Perform IDS for graph coloring."""
        for depth in range(1, self.num_nodes + 1):
            if self.dfs(0, depth):
                return self.colors
        return []

    def dfs(self, node: int, depth: int) -> bool:
        """Depth-limited DFS for graph coloring."""
        if node == self.num_nodes:
            return True

        if depth == 0:
            return False

        for color in range(self.num_colors):
            if self.is_valid_color(node, color):
                self.colors[node] = color
                if self.dfs(node + 1, depth - 1):
                    return True
                self.colors[node] = -1  # Backtrack

        return False


def read_adjacency_matrix(file_path: str) -> List[List[int]]:
    """Read adjacency matrix from a file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [list(map(int, line.split())) for line in lines]


def main():
    input_file = input("Enter the path to the adjacency matrix file: ")
    num_colors = int(input("Enter the number of colors: "))

    adjacency_matrix = read_adjacency_matrix(input_file)
    graph_coloring = GraphColoringIDS(adjacency_matrix, num_colors)

    solution = graph_coloring.ids_coloring()
    if solution:
        print("Solution found:", solution)
    else:
        print("No solution found with the given number of colors.")


if __name__ == "__main__":
    main()
