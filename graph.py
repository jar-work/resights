import networkx as nx

def generate_graph(data):
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

        for share in get_share_values(item['share']):
            graph.add_edge(source, target, share=share)

    return graph

def get_share_values(value):
    value = value.replace('%', '')

    if '-' in value:
        start, end = map(float, value.split('-'))
        average = (start + end) / 2
        return [start, average, end]
    if '<' in value:
        value = float(value.replace('<', ''))
        return [0, value/2, value]

    return [float(value)]
