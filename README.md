
# AI Knowledge Graph + Graph-CoT 推理增强版

本项目基于原始三元组抽取与知识图谱可视化流程，整合了结构化推理增强模块 —— Graph-CoT。
它通过“构图 → 路径发现 → LLM 多轮推理”实现更强的关系补全能力。

## 🧱 文件结构简要说明

| 文件名 | 说明 |
|--------|------|
| main.py | 主执行文件，支持 `--graphcot` 参数 |
| extractor.py | 提取三元组（复用原 prompt） |
| graph.py | 构建知识图谱结构（NetworkX） |
| reasoner.py | 生成两跳路径 |
| prompt.py | Graph‑CoT 专属 prompt 模板 |
| config.toml | 参数配置文件（新增 `[graphcot]` 配置段） |

## 🚀 运行示例

原始三元组抽取 + 可视化：
```bash
python main.py --input input.txt
```

启用 Graph-CoT 推理增强：
```bash
python main.py --input input.txt --graphcot
```

## ⚙️ 新增配置项说明（config.toml）

```toml
[graphcot]
enabled = true
max_path_length = 2
relationship_confidence = 0.6
```

- `max_path_length`: 当前仅支持 2 表示两跳路径推理（A→B→C）
- `relationship_confidence`: 暂留参数，未来用于 LLM 信任度阈值控制

## 📈 输出

- 三元组 JSON：`*.json`
- HTML 可视化图谱：`*.html`

## 📌 注意事项

- 需配置 OpenAI 或其他支持的 LLM API Key
- 所有推理都可选开启，不影响主流程稳定运行
