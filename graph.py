import networkx as nx

def generate_graph(data, company_full_name):
    graph = nx.DiGraph()

    for item in data:
        source = item['source']
        source_name = item['source_name']
        target = item['target']
        target_name = item['target_name']

        if not graph.has_node(source):
            graph.add_node(source, name=source_name)
        if not graph.has_node(target):
            graph.add_node(target, name=target_name)

        graph.add_edge(source, target)

    return graph
