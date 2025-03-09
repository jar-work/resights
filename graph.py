import networkx as nx
from colorama import Fore, Back, Style, init

def generate_graph(data):
    graph = nx.DiGraph()

    for item in data:
        source = item['source']
        source_name = item['source_name']
        source_depth = item['source_depth']
        target = item['target']
        target_name = item['target_name']
        target_depth = item['target_depth']

        if not graph.has_node(source):
            graph.add_node(source, name=source_name, depth=source_depth)
        if not graph.has_node(target):
            graph.add_node(target, name=target_name, depth=target_depth)

        shares = get_share_values(item['share'])
        graph.add_edge(
            source,
            target,
            lower_share=shares[0],
            middle_share=shares[1],
            upper_share=shares[2])

    return graph

def get_share_values(value):
    value = value.replace('%', '')

    if '-' in value:
        start, end = map(float, value.split('-'))
        start /= 100
        end /= 100
        average = (start + end) / 2
        return [start, average, end]
    if '<' in value:
        value = float(value.replace('<', ''))
        value /= 100
        return [0, value/2, value]

    value = float(value)/100
    return [value, value, value]

def get_ownership_description(source_name, lower_ownership, middle_ownership, upper_ownership, target_name):
    # if the three ownership values are equal, return the exact percentage
    if lower_ownership == middle_ownership and middle_ownership == upper_ownership:
        return f"{source_name} owns {middle_ownership * 100:.2f}% of {target_name}"

    # if the lower_ownership is zero, return the upper_ownership percentage as <
    if lower_ownership == 0:
        return f"{source_name} owns <{upper_ownership * 100:.2f}% of {target_name}"

    # return the range between lower_ownership and upper_ownership
    return f"{source_name} owns {lower_ownership * 100:.2f}-{upper_ownership * 100:.2f}% of {target_name}"


def print_ownership_structure(graph, source = None, target = None):
    # find the node with depth = 0
    focus_node = next(node for node, data in graph.nodes(data=True) if data['depth'] == 0)
    focus_node_name = graph.nodes[focus_node]['name']

    if source:
        print(Fore.GREEN + Back.BLACK + f"Ownership structure from {source} to {focus_node_name}:" + Style.RESET_ALL)
        source_node = next(node for node, data in graph.nodes(data=True) if data['name'] == source)
        path = nx.shortest_path(graph, source_node, focus_node)
        calculate_print_total_ownership(graph, path, source, focus_node)

    if target:
        print(Fore.GREEN + Back.BLACK + f"Ownership structure from {focus_node_name} to {target}:" + Style.RESET_ALL)
        target_node = next(node for node, data in graph.nodes(data=True) if data['name'] == target)
        path = nx.shortest_path(graph, focus_node, target_node)
        calculate_print_total_ownership(graph, path, focus_node_name, target_node)


def calculate_print_total_ownership(graph, path, source, target):
    total_lower_ownership = 1
    total_middle_ownership = 1
    total_upper_ownership = 1

    for i in range(len(path) - 1):
        source_name = graph.nodes[path[i]]['name']
        target_name = graph.nodes[path[i+1]]['name']
        lower_share = graph.edges[path[i], path[i+1]]['lower_share']
        middle_share = graph.edges[path[i], path[i + 1]]['middle_share']
        upper_share = graph.edges[path[i], path[i + 1]]['upper_share']

        total_lower_ownership *= lower_share
        total_middle_ownership *= middle_share
        total_upper_ownership *= upper_share

        print(get_ownership_description(source_name, lower_share, middle_share, upper_share, target_name))

    print(get_ownership_description(source, total_lower_ownership, total_middle_ownership, total_upper_ownership, graph.nodes[target]['name']))

