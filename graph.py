import networkx as nx
from enum import Enum, auto

class Direction(Enum):
    FROM = auto()
    TO = auto()

class Node:
    def __init__(self, source, name, depth):
        self.source = source
        self.name = name
        self.depth = depth

    def __hash__(self):
        return hash(self.source)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.source == other.source
        return False

class EdgeInformation:
    def __init__(self, share):
        self.lower_ownership = 0
        self.middle_ownership = 0
        self.upper_ownership = 0
        self.__calculate_share_values(share)

    def __calculate_share_values(self, share):
        value = share.replace('%', '')

        if '-' in value:
            start, end = map(float, value.split('-'))
            start /= 100
            end /= 100
            average = (start + end) / 2
            self.lower_ownership = start
            self.middle_ownership = average
            self.upper_ownership = end
            return
        if '<' in value:
            value = float(value.replace('<', ''))
            value /= 100
            self.lower_ownership = 0
            self.middle_ownership = value/2
            self.upper_ownership = value
            return

        value = float(value)/100
        self.lower_ownership = value
        self.middle_ownership = value
        self.upper_ownership = value

    def get_ownership_value(self):
        return EdgeInformation.calculate_ownership_value(self.lower_ownership, self.middle_ownership, self.upper_ownership)

    @staticmethod
    def calculate_ownership_value(lower_ownership, middle_ownership, upper_ownership):
        def format_percentage(value):
            if value <= 10:
                return f"{value:.2f}"
            return f"{value:.0f}"

        # if the three ownership values are equal, return the exact percentage
        if lower_ownership == middle_ownership and middle_ownership == upper_ownership:
            return f"{format_percentage(middle_ownership * 100)}%"

        # if the lower_ownership is zero, return the upper_ownership percentage as <
        if lower_ownership == 0:
            return f"<{format_percentage(upper_ownership * 100)}%"

        # return the range between lower_ownership and upper_ownership
        return f"{format_percentage(lower_ownership * 100)}-{format_percentage(upper_ownership * 100)}%"


def generate_graph(data):
    graph = nx.DiGraph()

    for item in data:
        source = Node(item['source'], item['source_name'], item['source_depth'])
        target = Node(item['target'], item['target_name'], item['target_depth'])

        if not graph.has_node(source):
            graph.add_node(source)
        if not graph.has_node(target):
            graph.add_node(target)

        edge_information = EdgeInformation(item['share'])
        graph.add_edge(
            source,
            target,
            data=edge_information)

    return graph

def get_ownership_structure(graph, node_name_to_check, direction: Direction):
    # find the node with depth = 0
    company_node = next(node for node, data in graph.nodes(data=True) if node.depth == 0)
    from_node = None
    to_node = None

    # if the node_to_check is not in the graph, return an empty generator
    if not any(node.name == node_name_to_check for node, _ in graph.nodes(data=True)):
        yield "Not found in the graph"
        return

    node_to_check = next(node for node, data in graph.nodes(data=True) if node.name == node_name_to_check)
    if direction == Direction.FROM:
        from_node = node_to_check
        to_node = company_node
    if direction == Direction.TO:
        from_node = company_node
        to_node = node_to_check

    path = nx.shortest_path(graph, from_node, to_node)
    yield from __calculate_get_total_ownership(graph, path, from_node, to_node)

def __calculate_get_total_ownership(graph, path, source, target):
    total_lower_ownership = 1
    total_middle_ownership = 1
    total_upper_ownership = 1

    for from_, to_ in zip(path, path[1:]):
        edge_information = graph.edges[from_, to_]['data']

        total_lower_ownership *= edge_information.lower_ownership
        total_middle_ownership *= edge_information.middle_ownership
        total_upper_ownership *= edge_information.upper_ownership

        yield f"{from_.name} owns {edge_information.get_ownership_value()} of {to_.name}"

    yield f" --> {source.name} owns {EdgeInformation.calculate_ownership_value(total_lower_ownership, total_middle_ownership, total_upper_ownership)} of {target.name}"

