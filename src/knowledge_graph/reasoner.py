def infer_relations(graph):
    two_hop_paths = graph.get_two_hop_paths()
    results = {}
    for a, b, c, path in two_hop_paths:
        results[(a, c)] = path
    return results.items()