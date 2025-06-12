#!/usr/bin/env python3
"""直接测试JSON序列化修复"""
import json
from dataclasses import dataclass, asdict

@dataclass
class DimensionAnalysis:
    """单个维度的分析结果"""
    dimension: str
    question: str
    answer: str
    sources: list = None
    requires_research: bool = False

# 测试原始对象（会失败）
test_obj = DimensionAnalysis(
    dimension="Q1",
    question="One-sentence Pitch",
    answer="测试答案",
    sources=["source1", "source2"],
    requires_research=False
)

print("测试 DimensionAnalysis 对象的 JSON 序列化：")
print("-" * 50)

try:
    # 直接序列化对象（会失败）
    json_str = json.dumps(test_obj)
    print("❌ 直接序列化：不应该成功")
except TypeError as e:
    print(f"✅ 直接序列化失败（预期）: {e}")

# 使用 asdict 转换后序列化（应该成功）
try:
    dict_obj = asdict(test_obj)
    json_str = json.dumps(dict_obj, ensure_ascii=False, indent=2)
    print("\n✅ 使用 asdict 转换后序列化成功：")
    print(json_str)
except Exception as e:
    print(f"❌ 使用 asdict 转换后序列化失败: {e}")

# 测试字典形式的序列化
results = {
    "Q1": test_obj,
    "Q2": test_obj
}

print("\n\n测试包含 DimensionAnalysis 对象的字典：")
print("-" * 50)

try:
    # 直接序列化（会失败）
    json_str = json.dumps(results)
    print("❌ 直接序列化字典：不应该成功")
except TypeError as e:
    print(f"✅ 直接序列化字典失败（预期）: {e}")

# 转换后序列化
try:
    dict_results = {key: asdict(value) for key, value in results.items()}
    json_str = json.dumps(dict_results, ensure_ascii=False, indent=2)
    print("\n✅ 转换后序列化字典成功：")
    print(json_str)
except Exception as e:
    print(f"❌ 转换后序列化字典失败: {e}")

print("\n✅ 修复验证完成！")