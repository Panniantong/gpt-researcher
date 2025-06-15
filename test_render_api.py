#!/usr/bin/env python3
"""
测试Render部署的GPT Researcher API
用于验证竞品调研功能是否正常工作
"""

import requests
import json
import time
from datetime import datetime

# 配置信息
RENDER_URL = "https://gpt-researcher-ec6o.onrender.com"  # 请替换为你的实际Render URL
# 例如: RENDER_URL = "https://gpt-researcher-abc123.onrender.com"
TIMEOUT = 300  # 5分钟超时

def test_health_check():
    """测试健康检查端点"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{RENDER_URL}/health", timeout=30)
        if response.status_code == 200:
            print("✅ 健康检查通过!")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {str(e)}")
        return False

def test_competitive_intelligence_summary(product_name="figma"):
    """测试基础竞品调研 (Summary)"""
    print(f"\n📊 测试基础竞品调研: {product_name}")
    
    # 请求数据
    request_data = {
        "task": product_name,
        "report_type": "competitive_intelligence",
        "report_source": "web",
        "tone": "Objective",
        "repo_name": "test",
        "branch_name": "main",
        "generate_in_background": False,  # 同步执行，等待结果
        "generate_files": False  # 新增：不生成文件，只返回文本内容
    }
    
    print(f"📤 发送请求...")
    print(f"   URL: {RENDER_URL}/report/")
    print(f"   数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{RENDER_URL}/report/",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  请求耗时: {duration:.2f}秒")
        print(f"📥 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 竞品调研成功!")
            
            # 显示关键信息
            print(f"   研究ID: {result.get('research_id', 'N/A')}")
            
            # 显示报告摘要（前500字符）
            report = result.get('report', '')
            if report:
                print(f"   报告摘要: {report[:500]}...")
            
            # 显示研究信息
            research_info = result.get('research_information', {})
            if research_info:
                print(f"   源URL数量: {len(research_info.get('source_urls', []))}")
                print(f"   访问URL数量: {len(research_info.get('visited_urls', []))}")
                print(f"   研究成本: ${research_info.get('research_costs', 0)}")
            
            # 显示文件路径（如果有的话）
            if 'docx_path' in result:
                print(f"   DOCX文件: {result.get('docx_path', 'N/A')}")
            if 'pdf_path' in result:
                print(f"   PDF文件: {result.get('pdf_path', 'N/A')}")

            # 如果没有文件路径，说明只返回了文本内容
            if 'docx_path' not in result and 'pdf_path' not in result:
                print("   📄 只返回文本内容，未生成文件")
            
            return True, result
        else:
            print(f"❌ 竞品调研失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时 (>{TIMEOUT}秒)")
        return False, None
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False, None

def test_competitive_intelligence_detailed(product_name="notion"):
    """测试详细竞品调研"""
    print(f"\n🔍 测试详细竞品调研: {product_name}")
    
    request_data = {
        "task": product_name,
        "report_type": "competitive_intelligence_detailed",
        "report_source": "web",
        "tone": "Analytical",
        "repo_name": "test",
        "branch_name": "main",
        "generate_in_background": False
    }
    
    print(f"📤 发送详细分析请求...")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{RENDER_URL}/report/",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  请求耗时: {duration:.2f}秒")
        print(f"📥 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 详细竞品调研成功!")
            
            # 显示关键信息
            print(f"   研究ID: {result.get('research_id', 'N/A')}")
            
            # 显示报告长度
            report = result.get('report', '')
            print(f"   报告长度: {len(report)} 字符")
            
            return True, result
        else:
            print(f"❌ 详细竞品调研失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ 详细调研异常: {str(e)}")
        return False, None

def test_competitive_intelligence_visual(product_name="claude.ai"):
    """测试可视化竞品调研"""
    print(f"\n🎨 测试可视化竞品调研: {product_name}")
    
    request_data = {
        "task": product_name,
        "report_type": "competitive_intelligence_visual",
        "report_source": "web",
        "tone": "Informative",
        "repo_name": "test",
        "branch_name": "main",
        "generate_in_background": False
    }
    
    print(f"📤 发送可视化分析请求...")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{RENDER_URL}/report/",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  请求耗时: {duration:.2f}秒")
        print(f"📥 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 可视化竞品调研成功!")
            
            # 显示关键信息
            print(f"   研究ID: {result.get('research_id', 'N/A')}")
            
            # 尝试解析JSON结构化数据
            report = result.get('report', '')
            if report:
                try:
                    # 如果报告是JSON格式，尝试解析
                    if report.startswith('{'):
                        json_data = json.loads(report)
                        print("   📊 JSON结构化数据:")
                        print(f"     - 产品名称: {json_data.get('metadata', {}).get('product_name', 'N/A')}")
                        print(f"     - 报告类型: {json_data.get('metadata', {}).get('report_type', 'N/A')}")
                        
                        # 显示Hero数据
                        hero_data = json_data.get('layer_1_hero', {}).get('hero_snapshot', {})
                        if hero_data:
                            print(f"     - 产品定位: {hero_data.get('tagline', 'N/A')}")
                            metrics = hero_data.get('key_metrics', {})
                            print(f"     - ARR: {metrics.get('arr', 'N/A')}")
                            print(f"     - 客户数: {metrics.get('clients', 'N/A')}")
                    else:
                        print(f"   报告长度: {len(report)} 字符")
                except:
                    print(f"   报告长度: {len(report)} 字符")
            
            return True, result
        else:
            print(f"❌ 可视化竞品调研失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ 可视化调研异常: {str(e)}")
        return False, None

def main():
    """主测试函数"""
    print("🚀 GPT Researcher Render API 测试")
    print("=" * 50)
    print(f"📍 测试URL: {RENDER_URL}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 请用户确认URL
    if "your-app-name" in RENDER_URL:
        print("⚠️  请先修改脚本中的RENDER_URL为你的实际Render URL!")
        print("   例如: https://gpt-researcher-abc123.onrender.com")
        return
    
    # 测试计数
    total_tests = 0
    passed_tests = 0
    
    # 1. 健康检查
    total_tests += 1
    if test_health_check():
        passed_tests += 1
    
    # 2. 基础竞品调研
    total_tests += 1
    success, _ = test_competitive_intelligence_summary("figma")
    if success:
        passed_tests += 1
    
    # 3. 详细竞品调研 (可选，耗时较长)
    print(f"\n❓ 是否继续测试详细竞品调研? (耗时较长)")
    # 为了自动化测试，这里跳过详细测试
    # total_tests += 1
    # success, _ = test_competitive_intelligence_detailed("notion")
    # if success:
    #     passed_tests += 1
    
    # 4. 可视化竞品调研 (可选)
    # total_tests += 1
    # success, _ = test_competitive_intelligence_visual("claude.ai")
    # if success:
    #     passed_tests += 1
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"   总测试数: {total_tests}")
    print(f"   通过测试: {passed_tests}")
    print(f"   失败测试: {total_tests - passed_tests}")
    print(f"   成功率: {(passed_tests/total_tests*100):.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过! API部署成功!")
    else:
        print("⚠️  部分测试失败，请检查配置和日志")
    
    print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
