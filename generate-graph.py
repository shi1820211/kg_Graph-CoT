import argparse
import os
import json

from src.knowledge_graph.extractor import llm_extract_from_main_style
from src.knowledge_graph.graph import KnowledgeGraph
from src.knowledge_graph.reasoner import infer_relations
from src.knowledge_graph.prompt import make_graph_cot_prompt
from src.knowledge_graph.visualization import visualize_knowledge_graph
from src.knowledge_graph.config import load_config


def run_graphcot_pipeline(config, input_text, debug=False):
    print("🚀 使用 Graph‑CoT 增强模式")
    
    # 抽取三元组
    triples = llm_extract_from_main_style(config, input_text, debug)

    # 构建图谱
    graph = KnowledgeGraph()
    graph.add_triples(triples)
    print(f"✅ 初始图构建完成：{len(graph.graph.nodes)} 个实体, {len(graph.graph.edges)} 条边")

    # 可选：推理增强（如你暂时不需要，可跳过）
    inferred = infer_relations(graph)
    for (s, o), path in inferred:
        prompt = make_graph_cot_prompt(s, o, path)
        print("\n==== 推理路径 ====")
        print(f"{s} → {' → '.join(path)} → {o}")
        print("Prompt:")
        print(prompt)

    return graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="输入文本或文本文件路径")
    parser.add_argument("--output", type=str, default="output.html", help="输出 HTML 文件路径")
    parser.add_argument("--triples", type=str, default=None, help="可选：输出三元组 JSON 文件路径")
    parser.add_argument("--debug", action="store_true", help="是否显示调试信息")
    args = parser.parse_args()

    # 读取输入
    if os.path.exists(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            input_text = f.read()
    else:
        input_text = args.input

    # 加载配置
    config = load_config()

    # 执行 pipeline
    graph = run_graphcot_pipeline(config, input_text, args.debug)

    # 导出可视化 HTML
    triples = graph.get_triples()
    visualize_knowledge_graph(triples, output_file=args.output, config=config)

    print(f"✅ 可视化文件已保存到: {args.output}")

    # 可选：导出三元组 JSON 文件
    if args.triples:
        with open(args.triples, "w", encoding="utf-8") as f:
            json.dump(triples, f, ensure_ascii=False, indent=2)
        print(f"📄 三元组已保存为: {args.triples}")


if __name__ == "__main__":
    main()
