#!/bin/bash

# 模型测试运行脚本
# Model testing runner script

echo "🚀 GPT-Researcher 模型可用性测试"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未找到，请先安装Python3"
    exit 1
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "❌ .env文件未找到，请先配置环境变量"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 提供测试选项
echo "请选择测试类型："
echo "1. 快速测试 (推荐) - 直接API调用测试"
echo "2. 完整测试 - 使用GPT-Researcher框架测试"
echo "3. 两个都运行"
echo ""

read -p "请输入选择 (1/2/3): " choice

case $choice in
    1)
        echo "🏃‍♂️ 运行快速测试..."
        python3 quick_model_test.py
        ;;
    2)
        echo "🔬 运行完整测试..."
        python3 test_models_availability.py
        ;;
    3)
        echo "🏃‍♂️ 运行快速测试..."
        python3 quick_model_test.py
        echo ""
        echo "🔬 运行完整测试..."
        python3 test_models_availability.py
        ;;
    *)
        echo "❌ 无效选择，默认运行快速测试"
        python3 quick_model_test.py
        ;;
esac

echo ""
echo "✅ 测试完成！"

# 检查是否生成了结果文件
if [ -f "model_test_results.json" ]; then
    echo "📄 详细结果已保存到: model_test_results.json"
fi
