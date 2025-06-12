#!/usr/bin/env python3
"""
调试embedding API响应
"""

import os
import sys
import logging
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置详细的日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_embedding_api():
    """测试embedding API的实际响应"""
    print("🔍 测试embedding API响应...")
    
    # 加载环境变量
    load_dotenv()
    
    try:
        from langchain_openai import OpenAIEmbeddings
        
        # 创建embedding实例
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_BASE_URL")
        )
        
        print(f"✅ 创建embedding实例成功")
        print(f"   API Key: {os.getenv('OPENAI_API_KEY')[:20]}...")
        print(f"   Base URL: {os.getenv('OPENAI_BASE_URL')}")
        print(f"   Model: text-embedding-3-large")
        
        # 测试单个查询
        test_text = "This is a test sentence."
        print(f"\n🧪 测试文本: '{test_text}'")
        
        try:
            result = embeddings.embed_query(test_text)
            
            print(f"\n📊 API响应分析:")
            print(f"   响应类型: {type(result)}")
            print(f"   响应长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
            
            if result is None:
                print("   ❌ 响应为None")
            elif isinstance(result, list):
                if len(result) > 0:
                    print(f"   ✅ 响应是列表，长度: {len(result)}")
                    print(f"   前5个值: {result[:5]}")
                    print(f"   值的类型: {[type(x) for x in result[:5]]}")
                    
                    # 检查是否都是数字
                    all_numeric = all(isinstance(x, (int, float)) for x in result)
                    print(f"   所有值都是数字: {all_numeric}")
                    
                    if not all_numeric:
                        non_numeric = [x for x in result[:10] if not isinstance(x, (int, float))]
                        print(f"   非数字值示例: {non_numeric}")
                else:
                    print("   ❌ 响应是空列表")
            else:
                print(f"   ❌ 响应不是列表: {str(result)[:200]}...")
                
        except Exception as e:
            print(f"   ❌ embed_query调用失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试多个文档
        print(f"\n🧪 测试多个文档...")
        test_docs = ["First document", "Second document"]
        
        try:
            result = embeddings.embed_documents(test_docs)
            
            print(f"\n📊 多文档API响应分析:")
            print(f"   响应类型: {type(result)}")
            print(f"   响应长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
            
            if result is None:
                print("   ❌ 响应为None")
            elif isinstance(result, list):
                print(f"   ✅ 响应是列表，包含 {len(result)} 个embedding")
                for i, embedding in enumerate(result[:2]):
                    print(f"   Embedding {i+1}:")
                    print(f"     类型: {type(embedding)}")
                    print(f"     长度: {len(embedding) if hasattr(embedding, '__len__') else 'N/A'}")
                    if isinstance(embedding, list) and len(embedding) > 0:
                        print(f"     前5个值: {embedding[:5]}")
                        all_numeric = all(isinstance(x, (int, float)) for x in embedding)
                        print(f"     所有值都是数字: {all_numeric}")
            else:
                print(f"   ❌ 响应不是列表: {str(result)[:200]}...")
                
        except Exception as e:
            print(f"   ❌ embed_documents调用失败: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ 创建embedding实例失败: {e}")
        import traceback
        traceback.print_exc()

def test_robust_embedding():
    """测试robust embedding包装器"""
    print(f"\n🔧 测试robust embedding包装器...")
    
    try:
        from gpt_researcher.memory.robust_embeddings import create_robust_embeddings
        
        # 创建robust embedding
        robust_embeddings = create_robust_embeddings(
            "openai", 
            "text-embedding-3-large",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_BASE_URL")
        )
        
        if robust_embeddings:
            print("✅ 创建robust embedding成功")
            
            # 测试查询
            test_text = "Test with robust wrapper"
            result = robust_embeddings.embed_query(test_text)
            
            print(f"📊 Robust embedding结果:")
            print(f"   类型: {type(result)}")
            print(f"   长度: {len(result) if hasattr(result, '__len__') else 'N/A'}")
            if isinstance(result, list) and len(result) > 0:
                print(f"   前5个值: {result[:5]}")
        else:
            print("❌ 创建robust embedding失败")
            
    except Exception as e:
        print(f"❌ 测试robust embedding失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 开始调试embedding API...")
    test_embedding_api()
    test_robust_embedding()
    print("\n✅ 调试完成")
