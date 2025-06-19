import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._triples = []  # 用于保存原始三元组

    def add_triples(self, triples):
        for triple in triples:
            # 支持三元组为 tuple 或 dict 类型
            if isinstance(triple, dict):
                h, r, t = triple["subject"], triple["predicate"], triple["object"]
            else:
                h, r, t = triple
            self.graph.add_edge(h, t, label=r)
            self._triples.append({"subject": h, "predicate": r, "object": t})

    def get_triples(self):
        return self._triples

    def get_two_hop_paths(self):
        paths = []
        for source in self.graph.nodes:
            for intermediate in self.graph.successors(source):
                for target in self.graph.successors(intermediate):
                    if source != target:
                        paths.append((source, intermediate, target, [source, intermediate, target]))
        return paths
