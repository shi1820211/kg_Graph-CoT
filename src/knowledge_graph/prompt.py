def make_graph_cot_prompt(existing_triples, inferred_paths, path, new_triples):
    return f"""
你是一个知识图谱专家。我们目前提取了以下三元组：
{existing_triples}

我们从图结构中发现了如下可能的推理路径：
{inferred_paths}

当前你需要关注的推理路径为：
{path}

基于此路径，判断是否可以推理出新的三元组，如果可以，请在如下格式中补充：
新增三元组：
(主语, 谓语, 宾语)
"""