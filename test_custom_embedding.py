#!/usr/bin/env python3
"""
测试自定义embedding修复
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_custom_embedding():
    """测试自定义embedding客户端"""
    print("🧪 测试自定义embedding客户端...")
    
    # 加载环境变量
    load_dotenv()
    
    try:
        from gpt_researcher.memory.custom_embeddings import create_custom_embeddings
        
        # 创建自定义embedding实例
        embeddings = create_custom_embeddings(
            model="text-embedding-3-large",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        
        print("✅ 创建自定义embedding实例成功")
        
        # 测试单个查询
        test_text = "This is a test sentence for custom embedding."
        print(f"\n🔍 测试文本: '{test_text}'")
        
        result = embeddings.embed_query(test_text)
        
        print(f"📊 结果分析:")
        print(f"   类型: {type(result)}")
        print(f"   长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
        
        if isinstance(result, list) and len(result) > 0:
            print(f"   前5个值: {result[:5]}")
            all_numeric = all(isinstance(x, (int, float)) for x in result)
            print(f"   所有值都是数字: {all_numeric}")
            
            if all_numeric and len(result) > 100:  # 合理的embedding长度
                print("   ✅ 单个查询embedding成功！")
            else:
                print("   ❌ embedding格式不正确")
        else:
            print("   ❌ 返回结果不是有效的embedding")
        
        # 测试多个文档
        print(f"\n🔍 测试多个文档...")
        test_docs = ["First document for testing", "Second document for testing"]
        
        results = embeddings.embed_documents(test_docs)
        
        print(f"📊 多文档结果分析:")
        print(f"   类型: {type(results)}")
        print(f"   数量: {len(results) if hasattr(results, '__len__') else 'N/A'}")
        
        if isinstance(results, list) and len(results) == len(test_docs):
            all_valid = True
            for i, embedding in enumerate(results):
                if isinstance(embedding, list) and len(embedding) > 0:
                    all_numeric = all(isinstance(x, (int, float)) for x in embedding)
                    print(f"   文档{i+1}: 长度={len(embedding)}, 数字={all_numeric}")
                    if not all_numeric:
                        all_valid = False
                else:
                    print(f"   文档{i+1}: 无效格式")
                    all_valid = False
            
            if all_valid:
                print("   ✅ 多文档embedding成功！")
            else:
                print("   ❌ 部分embedding格式不正确")
        else:
            print("   ❌ 返回结果数量不匹配")
            
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_integration():
    """测试与Memory类的集成"""
    print(f"\n🧪 测试Memory类集成...")
    
    try:
        from gpt_researcher.memory.embeddings import Memory
        from gpt_researcher.config import Config
        
        # 创建配置
        config = Config()
        print(f"Embedding provider: {config.embedding_provider}")
        print(f"Embedding model: {config.embedding_model}")
        
        # 创建Memory实例
        memory = Memory(
            embedding_provider=config.embedding_provider,
            model=config.embedding_model
        )
        
        print("✅ 创建Memory实例成功")
        
        # 获取embeddings对象
        embeddings = memory.get_embeddings()
        print(f"Embeddings类型: {type(embeddings)}")
        
        # 测试embedding
        test_text = "Integration test with Memory class"
        result = embeddings.embed_query(test_text)
        
        if isinstance(result, list) and len(result) > 0:
            print(f"✅ Memory集成测试成功！embedding长度: {len(result)}")
            return True
        else:
            print("❌ Memory集成测试失败")
            return False
            
    except Exception as e:
        print(f"❌ Memory集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 开始测试自定义embedding修复...")
    
    success1 = test_custom_embedding()
    success2 = test_memory_integration()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！embedding问题已修复")
    else:
        print("\n❌ 部分测试失败，需要进一步调试")
    
    print("\n✅ 测试完成")
