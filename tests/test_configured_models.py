#!/usr/bin/env python3
"""
配置模型测试脚本
专门测试default.py中配置的具体模型是否在逆向API中可用
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 加载环境变量
load_dotenv()

def get_available_models():
    """获取逆向API中可用的模型列表"""
    print("🔍 获取逆向API可用模型列表...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL', 'https://gptgod.cloud/v1')
    
    if not api_key:
        print("  ❌ OPENAI_API_KEY 未设置")
        return []
    
    try:
        url = f"{base_url}/models"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            model_ids = [model.get('id', '') for model in models]
            print(f"  ✅ 成功获取 {len(model_ids)} 个模型")
            return model_ids
        else:
            print(f"  ❌ 请求失败: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"  ❌ 获取模型列表失败: {e}")
        return []

def test_specific_model(model_name, available_models):
    """测试特定模型是否可用"""
    print(f"\n🧪 测试模型: {model_name}")
    
    # 检查模型是否在可用列表中
    if model_name not in available_models:
        print(f"  ❌ 模型 '{model_name}' 不在可用模型列表中")
        
        # 寻找相似的模型名
        similar_models = [m for m in available_models if model_name.lower() in m.lower() or m.lower() in model_name.lower()]
        if similar_models:
            print(f"  💡 找到相似模型: {similar_models[:3]}")
        return False
    
    # 尝试调用模型
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL', 'https://gptgod.cloud/v1')
    
    try:
        url = f"{base_url}/chat/completions"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": "请简单回答：你好"}
            ],
            "max_tokens": 20,
            "temperature": 0.1
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"  ✅ 模型测试成功！")
                print(f"  💬 响应: {content.strip()}")
                return True
            else:
                print(f"  ❌ 响应格式异常")
                return False
        else:
            print(f"  ❌ 请求失败: HTTP {response.status_code}")
            error_info = response.text[:200]
            print(f"  📝 错误信息: {error_info}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 GPT-Researcher 配置模型测试工具")
    print("=" * 60)
    
    # 从default.py中读取配置的模型
    configured_models = {
        "FAST_LLM": "gpt-4o-mini",      # 从 "openai:gpt-4o-mini" 提取
        "SMART_LLM": "gpt-4.1",         # 从 "openai:gpt-4.1" 提取  
        "STRATEGIC_LLM": "o4-mini",     # 从 "openai:o4-mini" 提取
        "O3_LLM": "o3",                 # 新增 o3 测试
        "O1_LLM": "o1",                 # 新增 o1 测试
    }
    
    print("\n📋 项目中配置的模型:")
    for config_name, model_name in configured_models.items():
        print(f"  {config_name}: {model_name}")
    
    print("\n" + "=" * 60)
    
    # 获取可用模型列表
    available_models = get_available_models()
    
    if not available_models:
        print("❌ 无法获取可用模型列表，无法继续测试")
        return
    
    # 显示部分可用模型
    print(f"\n📊 API中可用的模型示例 (共{len(available_models)}个):")
    for i, model in enumerate(available_models[:10]):
        print(f"  {i+1:2d}. {model}")
    if len(available_models) > 10:
        print(f"  ... 还有 {len(available_models) - 10} 个模型")
    
    print("\n" + "=" * 60)
    
    # 测试每个配置的模型
    results = {}
    for config_name, model_name in configured_models.items():
        success = test_specific_model(model_name, available_models)
        results[config_name] = {
            "model": model_name,
            "success": success
        }
    
    # 显示测试结果总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print("=" * 60)
    
    success_count = 0
    for config_name, result in results.items():
        status = "✅ 可用" if result["success"] else "❌ 不可用"
        print(f"  {config_name:15} | {result['model']:15} | {status}")
        if result["success"]:
            success_count += 1
    
    print("-" * 60)
    print(f"总计: {success_count}/{len(results)} 个配置模型可用")
    
    # 给出建议
    if success_count == len(results):
        print("🎉 所有配置的模型都可以正常使用！")
    elif success_count > 0:
        print("⚠️  部分模型可用，建议:")
        for config_name, result in results.items():
            if not result["success"]:
                print(f"    - 检查 {config_name} 的模型名称: {result['model']}")
                # 建议替代模型
                model_name = result['model']
                suggestions = []
                for available in available_models:
                    if 'gpt-4' in available.lower() and 'gpt-4' in model_name.lower():
                        suggestions.append(available)
                    elif 'gpt-3' in available.lower() and 'gpt-3' in model_name.lower():
                        suggestions.append(available)
                    elif model_name.lower() in available.lower():
                        suggestions.append(available)
                
                if suggestions:
                    print(f"      建议替代模型: {suggestions[:3]}")
    else:
        print("🚨 所有配置的模型都不可用！")
        print("💡 建议:")
        print("  1. 检查逆向API是否支持这些模型")
        print("  2. 查看可用模型列表，选择合适的替代模型")
        print("  3. 更新 gpt_researcher/config/variables/default.py 中的模型配置")
    
    print("\n💡 如需修改模型配置，请编辑文件:")
    print("   gpt_researcher/config/variables/default.py")
    print("   修改 FAST_LLM, SMART_LLM, STRATEGIC_LLM 的值")

if __name__ == "__main__":
    main()
