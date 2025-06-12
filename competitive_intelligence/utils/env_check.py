"""
环境变量检查工具
"""
import os


def check_environment():
    """
    检查必要的环境变量
    
    Returns:
        tuple: (is_valid, missing_vars, warnings)
    """
    required_vars = ["OPENAI_API_KEY"]  # 或其他LLM的密钥
    optional_vars = ["TAVILY_API_KEY", "SERPER_API_KEY", "GOOGLE_API_KEY"]
    
    missing_required = []
    missing_optional = []
    warnings = []
    
    # 检查必需的变量
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    # 检查可选的搜索API
    search_apis_found = False
    for var in optional_vars:
        if os.getenv(var):
            search_apis_found = True
        else:
            missing_optional.append(var)
    
    if not search_apis_found:
        warnings.append("未找到搜索API密钥，将无法进行网络搜索。建议设置 TAVILY_API_KEY")
    
    is_valid = len(missing_required) == 0
    
    return is_valid, missing_required, warnings


def print_env_status():
    """打印环境变量状态"""
    is_valid, missing_required, warnings = check_environment()
    
    print("🔍 环境变量检查")
    print("=" * 40)
    
    if is_valid:
        print("✅ 必需的环境变量已设置")
    else:
        print("❌ 缺少必需的环境变量:")
        for var in missing_required:
            print(f"   - {var}")
    
    if warnings:
        print("\n⚠️  警告:")
        for warning in warnings:
            print(f"   - {warning}")
    
    print("\n💡 提示:")
    print("   export OPENAI_API_KEY='your-key'")
    print("   export TAVILY_API_KEY='your-key'  # 用于网络搜索")
    
    return is_valid