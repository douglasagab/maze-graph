from maze import Maze, Node


def average_corridor_length(nodes):
    neighbors = {}
    degree = {}

    for node in nodes:
        reachable = node.get_reachable_neighbors()
        neighbors[id(node)] = reachable
        degree[id(node)] = len(reachable)

    lengths = []
    seen = set()

    for node in nodes:
        node_id = id(node)
        if degree[node_id] == 2:
            continue

        for start in neighbors[node_id]:
            if (node_id, id(start)) in seen or (id(start), node_id) in seen:
                continue

            if degree[id(start)] != 2:
                seen.add((node_id, id(start)))
                continue

            length = 0
            prev = node
            current = start
            chain = set()

            while degree[id(current)] == 2 and id(current) not in chain:
                chain.add(id(current))
                length += 1
                seen.add((id(prev), id(current)))

                nxt = None
                for candidate in neighbors[id(current)]:
                    if candidate is not prev:
                        nxt = candidate
                        break

                if nxt is None:
                    break

                prev = current
                current = nxt

            seen.add((id(prev), id(current)))

            if degree[id(current)] != 2:
                lengths.append(length)

    if not lengths:
        return 0.0

    return sum(lengths) / len(lengths)


class MazeData:
    def __init__(self):
        self.total_nodes = 0
        self.expanded_nodes = 0
        self.discoverd_nodes = 0
        self.total_edges = 0
        self.degrees = [0, 0, 0, 0]

    def collect_from(self, maze: Maze):
        nodes = []

        def collect(node: Node):
            self.total_nodes += 1
            nodes.append(node)

            if node.state == "DISCOVERED":
                self.discoverd_nodes += 1
            elif node.state == "EXPANDED":
                self.expanded_nodes += 1

            degree = len(node.get_reachable_neighbors())
            self.degrees[degree - 1] += 1
            self.total_edges += degree

        maze.apply_for_each_node(lambda node: collect(node))

        self.average_degree = self.total_edges / self.total_nodes
        self.average_corridor_length = average_corridor_length(nodes)
        self.build_time = maze.build_time
        self.solve_time = maze.solve_time
        self.total_dead_ends = self.degrees[0]


    def print_data(self):
        print(self.degrees)

        print(
            f"expanded: {self.expanded_nodes}\ndiscovered: {self.discoverd_nodes}\nedges: {self.total_edges}\ntotal_dead_ends: {self.total_dead_ends}\naverage_degree: {self.average_degree}\naverage_corridor_length: {self.average_corridor_length}\nsolve_time: {self.solve_time}\nbuild_time:{self.build_time}"
        )
