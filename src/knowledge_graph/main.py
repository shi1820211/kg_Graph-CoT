import argparse
import os

from src.knowledge_graph.extractor import llm_extract_from_main_style
from src.knowledge_graph.graph import KnowledgeGraph
from src.knowledge_graph.reasoner import infer_relations
from src.knowledge_graph.prompt import make_graph_cot_prompt

def load_config():
    import toml
    return toml.load("config.toml")

def run_graphcot_pipeline(config, input_text, debug=False):
    print("🚀 使用 Graph‑CoT 增强模式")

    # 调用 LLM 抽取三元组
    triples = llm_extract_from_main_style(config, input_text, debug)

    # 构建知识图谱对象并添加三元组
    graph = KnowledgeGraph()
    graph.add_triples(triples)

    print(f"✅ 初始图构建完成：{len(graph.graph.nodes)} 个实体, {len(graph.graph.edges)} 条边")

    # 关系推理（可选）
    inferred = infer_relations(graph)
    for (s, o), path in inferred:
        prompt = make_graph_cot_prompt(s, o, path)
        print("\n==== 推理路径 ====")
        print(f"{s} → {' → '.join(path)} → {o}")
        print("Prompt:")
        print(prompt)

    return graph  # ✅ 返回图对象，供外部调用保存或可视化

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="输入文本或文本文件路径")
    parser.add_argument("--debug", action="store_true", help="是否显示调试信息")
    args = parser.parse_args()

    # 读取输入文本
    if os.path.exists(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            input_text = f.read()
    else:
        input_text = args.input

    # 加载配置
    config = load_config()

    # 执行图谱构建
    run_graphcot_pipeline(config, input_text, args.debug)

if __name__ == "__main__":
    main()
