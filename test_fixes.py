#!/usr/bin/env python3
"""
测试修复的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gpt_researcher.scraper.utils import parse_dimension

def test_parse_dimension():
    """测试图片维度解析修复"""
    print("🧪 测试图片维度解析修复...")

    # 测试用例
    test_cases = [
        ("268.29694323144105", 268),
        ("771.6923076923077", 771),
        ("803.2", 803),
        ("1139.5348837209303", 1139),
        ("800px", 800),
        ("500.5px", 500),
        ("", None),
        ("invalid", None),
        (None, None),
        ("100", 100),
        # 新增的CSS值测试用例
        ("100%", None),
        ("auto", None),
        ("inherit", None),
        ("50vw", None),
        ("2em", None),
        ("1.5rem", None),
        ("initial", None),
        ("unset", None),
        ("none", None)
    ]
    
    all_passed = True
    for input_val, expected in test_cases:
        try:
            result = parse_dimension(input_val)
            if result == expected:
                print(f"✅ {input_val} -> {result} (期望: {expected})")
            else:
                print(f"❌ {input_val} -> {result} (期望: {expected})")
                all_passed = False
        except Exception as e:
            print(f"❌ {input_val} -> 异常: {e}")
            all_passed = False
    
    return all_passed

def test_robust_embeddings():
    """测试嵌入修复"""
    print("\n🧪 测试嵌入修复...")

    try:
        from gpt_researcher.memory.robust_embeddings import RobustOpenAIEmbeddings
        from langchain_openai import OpenAIEmbeddings

        # 创建基础嵌入
        base_embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key="sk-test",  # 测试密钥
            openai_api_base="https://api.openai.com/v1"
        )

        # 创建健壮嵌入包装器
        robust_embeddings = RobustOpenAIEmbeddings(base_embeddings)

        print("✅ RobustOpenAIEmbeddings 创建成功")

        # 测试维度获取
        dimension = robust_embeddings._get_dimension()
        print(f"✅ 获取维度: {dimension}")

        return True

    except Exception as e:
        print(f"❌ 嵌入测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔧 开始测试修复...")
    
    # 测试图片维度解析
    dimension_test_passed = test_parse_dimension()
    
    # 测试嵌入修复
    embedding_test_passed = test_robust_embeddings()
    
    print("\n📊 测试结果:")
    print(f"图片维度解析: {'✅ 通过' if dimension_test_passed else '❌ 失败'}")
    print(f"嵌入修复: {'✅ 通过' if embedding_test_passed else '❌ 失败'}")
    
    if dimension_test_passed and embedding_test_passed:
        print("\n🎉 所有修复测试通过！")
        return True
    else:
        print("\n⚠️ 部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    main()
