"""
分析 GPT Researcher 的成本计算
目标：解释 $0.015838300000000003 这个成本是如何计算出来的
"""

# 从 gpt_researcher/utils/costs.py 的价格常量
INPUT_COST_PER_TOKEN = 0.000005    # 每个输入 token 的成本
OUTPUT_COST_PER_TOKEN = 0.000015   # 每个输出 token 的成本
EMBEDDING_COST = 0.02 / 1000000    # 每个嵌入 token 的成本 (ada-3-small)

# 总成本
TOTAL_COST = 0.015838300000000003

print("GPT Researcher 成本分析")
print("=" * 60)
print(f"总成本: ${TOTAL_COST}")
print("\n价格设置:")
print(f"- 输入 token 价格: ${INPUT_COST_PER_TOKEN} / token")
print(f"- 输出 token 价格: ${OUTPUT_COST_PER_TOKEN} / token") 
print(f"- 嵌入 token 价格: ${EMBEDDING_COST} / token")
print()

# 反推可能的 token 使用量
print("成本分解分析:")
print("-" * 60)

# 情况 1: 只有 LLM 成本（输入+输出）
# 假设输出 token 是输入 token 的 1/4
print("\n1. 假设只有 LLM 成本:")
# TOTAL = input_tokens * INPUT_COST + output_tokens * OUTPUT_COST
# 假设 output_tokens = input_tokens / 4
# TOTAL = input_tokens * INPUT_COST + (input_tokens/4) * OUTPUT_COST
# TOTAL = input_tokens * (INPUT_COST + OUTPUT_COST/4)
input_tokens_only_llm = TOTAL_COST / (INPUT_COST_PER_TOKEN + OUTPUT_COST_PER_TOKEN/4)
output_tokens_only_llm = input_tokens_only_llm / 4
print(f"   输入 tokens: {input_tokens_only_llm:.0f}")
print(f"   输出 tokens: {output_tokens_only_llm:.0f}")
print(f"   验证: ${input_tokens_only_llm * INPUT_COST_PER_TOKEN + output_tokens_only_llm * OUTPUT_COST_PER_TOKEN:.6f}")

# 情况 2: LLM + 嵌入成本
print("\n2. 假设有 LLM + 嵌入成本:")
# 假设嵌入使用了 10000 tokens
embedding_tokens = 10000
embedding_cost = embedding_tokens * EMBEDDING_COST
remaining_cost = TOTAL_COST - embedding_cost
print(f"   嵌入 tokens: {embedding_tokens}")
print(f"   嵌入成本: ${embedding_cost:.6f}")
print(f"   剩余 LLM 成本: ${remaining_cost:.6f}")

# 计算 LLM tokens
input_tokens_with_embed = remaining_cost / (INPUT_COST_PER_TOKEN + OUTPUT_COST_PER_TOKEN/4)
output_tokens_with_embed = input_tokens_with_embed / 4
print(f"   LLM 输入 tokens: {input_tokens_with_embed:.0f}")
print(f"   LLM 输出 tokens: {output_tokens_with_embed:.0f}")

# 情况 3: 更真实的场景 - 多次 LLM 调用
print("\n3. 多次 LLM 调用场景:")
print("   一次研究可能包括:")
print("   - 1次 agent 选择")
print("   - 1次 研究大纲规划") 
print("   - 3-5次 内容检索和处理")
print("   - 1次 报告生成")
print("   - 多次嵌入计算")

# 模拟真实场景
agent_selection = {"input": 500, "output": 100}
outline_planning = {"input": 1000, "output": 500}
content_retrieval = {"input": 2000, "output": 1000}  # 每次
report_generation = {"input": 3000, "output": 2000}
embedding_docs = 20000  # 嵌入文档的 tokens

total_input_tokens = (
    agent_selection["input"] + 
    outline_planning["input"] + 
    content_retrieval["input"] * 4 +  # 假设4次检索
    report_generation["input"]
)
total_output_tokens = (
    agent_selection["output"] + 
    outline_planning["output"] + 
    content_retrieval["output"] * 4 +
    report_generation["output"]
)

llm_cost = total_input_tokens * INPUT_COST_PER_TOKEN + total_output_tokens * OUTPUT_COST_PER_TOKEN
embed_cost = embedding_docs * EMBEDDING_COST
total_calculated = llm_cost + embed_cost

print(f"\n   详细分解:")
print(f"   - Agent 选择: {agent_selection['input']} + {agent_selection['output']} tokens")
print(f"   - 大纲规划: {outline_planning['input']} + {outline_planning['output']} tokens")
print(f"   - 内容检索 (4次): {content_retrieval['input']*4} + {content_retrieval['output']*4} tokens")
print(f"   - 报告生成: {report_generation['input']} + {report_generation['output']} tokens")
print(f"   - 文档嵌入: {embedding_docs} tokens")
print(f"\n   总计:")
print(f"   - 输入 tokens: {total_input_tokens}")
print(f"   - 输出 tokens: {total_output_tokens}")
print(f"   - 嵌入 tokens: {embedding_docs}")
print(f"\n   成本计算:")
print(f"   - LLM 成本: ${llm_cost:.6f}")
print(f"   - 嵌入成本: ${embed_cost:.6f}")
print(f"   - 总成本: ${total_calculated:.6f}")
print(f"   - 与目标差异: ${abs(total_calculated - TOTAL_COST):.6f}")

# 情况 4: 根据实际成本反推最可能的 token 分布
print("\n4. 反推最可能的 token 使用量:")
# 假设嵌入占总成本的 1%
estimated_embed_cost = TOTAL_COST * 0.01
estimated_llm_cost = TOTAL_COST - estimated_embed_cost
estimated_embed_tokens = estimated_embed_cost / EMBEDDING_COST

# 假设输出是输入的 40%
# llm_cost = input * INPUT_COST + output * OUTPUT_COST
# llm_cost = input * INPUT_COST + (input * 0.4) * OUTPUT_COST
# llm_cost = input * (INPUT_COST + 0.4 * OUTPUT_COST)
estimated_input_tokens = estimated_llm_cost / (INPUT_COST_PER_TOKEN + 0.4 * OUTPUT_COST_PER_TOKEN)
estimated_output_tokens = estimated_input_tokens * 0.4

print(f"   估计的嵌入 tokens: {estimated_embed_tokens:.0f}")
print(f"   估计的输入 tokens: {estimated_input_tokens:.0f}")
print(f"   估计的输出 tokens: {estimated_output_tokens:.0f}")
print(f"\n   验证计算:")
verify_llm = estimated_input_tokens * INPUT_COST_PER_TOKEN + estimated_output_tokens * OUTPUT_COST_PER_TOKEN
verify_embed = estimated_embed_tokens * EMBEDDING_COST
verify_total = verify_llm + verify_embed
print(f"   - LLM 成本: ${verify_llm:.6f}")
print(f"   - 嵌入成本: ${verify_embed:.6f}")
print(f"   - 总计: ${verify_total:.6f}")

print("\n" + "=" * 60)
print("结论:")
print(f"成本 ${TOTAL_COST} 最可能来自:")
print(f"1. 约 {estimated_input_tokens:.0f} 个输入 tokens")
print(f"2. 约 {estimated_output_tokens:.0f} 个输出 tokens")
print(f"3. 约 {estimated_embed_tokens:.0f} 个嵌入 tokens")
print("\n这相当于:")
print(f"- 处理了约 {estimated_input_tokens/1000:.1f}k 字的输入文本")
print(f"- 生成了约 {estimated_output_tokens/1000:.1f}k 字的输出文本")
print(f"- 嵌入了约 {estimated_embed_tokens/1000:.1f}k 字的文档")