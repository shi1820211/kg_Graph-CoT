"""
LLM extractor module - 提供用于原项目兼容的三元组抽取函数
"""

from src.knowledge_graph.prompts import MAIN_SYSTEM_PROMPT, MAIN_USER_PROMPT
from src.knowledge_graph.llm import call_llm, extract_json_from_text

def llm_extract_from_main_style(config, full_text, debug=False):
    """
    仿照 main.py 的逻辑，兼容原有 config 的三元组抽取函数
    """
    system_prompt = MAIN_SYSTEM_PROMPT
    user_prompt = MAIN_USER_PROMPT + "```\n" + full_text + "\n```"


    model = config["llm"]["model"]
    api_key = config["llm"]["api_key"]
    base_url = config["llm"]["base_url"]
    max_tokens = config["llm"]["max_tokens"]
    temperature = config["llm"]["temperature"]
    enable_think = config["llm"].get("enable_think", True)

    response = call_llm(
        config,
        model=model,
        user_prompt=user_prompt,
        api_key=api_key,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        base_url=base_url,
        enable_thinking=enable_think,
    )

    if debug:
        print("Raw LLM response:")
        print(response)

    result = extract_json_from_text(response)
    return result or []
