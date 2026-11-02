class MazeData:
    def __init__(self):
        self.total_nodes = 0
        self.expanded_nodes = 0
        self.discoverd_nodes = 0
        self.total_edges = 0
        self.degrees = [0, 0, 0, 0]
        self.total_dead_ends = 0

    def collect_from(self, maze: Maze):
        def collect(node: Node):
            self.total_nodes += 1 

            if node.state == "DISCOVERED":
                self.discoverd_nodes += 1
            elif node.state == "EXPANDED":
                self.expanded_nodes += 1

            if node.is_dead_end():
                self.total_dead_ends += 1

            degree = len(node.get_reachable_neighbors())
            self.degrees[degree - 1] += 1
            self.total_edges += degree

        maze.apply_for_each_node(lambda node: collect(node))

        self.average_degree = self.total_edges / self.total_nodes
        self.build_time = maze.build_time
        self.solve_time = maze.solve_time

    def print_data(self):
        print(self.degrees)

        print(
            f"expanded: {self.expanded_nodes}\ndiscovered: {self.discoverd_nodes}\nedges: {self.total_edges}\ntotal_dead_ends: {self.total_dead_ends}\naverage_degree: {self.average_degree}\nsolve_time: {self.solve_time}\nbuild_time:{self.build_time}"
        )
