import networkx as nx

from models.direction import Direction
from models.edge_information import EdgeInformation
from models.node import Node

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

    total_lower_ownership = 1
    total_middle_ownership = 1
    total_upper_ownership = 1

    for from_, to_ in zip(path, path[1:]):
        edge_information = graph.edges[from_, to_]['data']

        total_lower_ownership *= edge_information.lower_ownership
        total_middle_ownership *= edge_information.middle_ownership
        total_upper_ownership *= edge_information.upper_ownership

        yield f"{from_.name} owns {edge_information.get_ownership_value()} of {to_.name}"

    yield f" --> {from_node.name} owns {EdgeInformation.calculate_ownership_value(total_lower_ownership, total_middle_ownership, total_upper_ownership)} of {to_node.name}"

