#!/usr/bin/env python3
"""
演示 re.search() 返回的 Match 对象的不同属性
"""

import re
import json

# 模拟一个包含JSON的响应
response = '''
这是一些文本内容，然后有一个JSON：
{
    "team_size": {
        "value": "48",
        "source": "https://getlatka.com/companies/gadget.dev"
    },
    "one_liner": {
        "value": "Info insufficient",
        "source": "Info insufficient"
    }
}
还有一些其他文本内容。
'''

print("原始响应:")
print(response)
print("\n" + "="*50 + "\n")

# 使用正则表达式匹配JSON
json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)

if json_match:
    print("1. json_match.group() - 匹配到的JSON部分:")
    json_part = json_match.group()
    print(repr(json_part))
    print("\n实际内容:")
    print(json_part)
    
    print("\n" + "-"*30 + "\n")
    
    print("2. json_match.string - 整个原始字符串:")
    original_string = json_match.string
    print(repr(original_string[:100]) + "...")  # 只显示前100个字符
    
    print("\n" + "-"*30 + "\n")
    
    print("3. 尝试解析JSON:")
    
    # 正确的方式 - 使用 group()
    try:
        parsed_json = json.loads(json_match.group())
        print("✅ 使用 json_match.group() 成功:")
        print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"❌ 使用 json_match.group() 失败: {e}")
    
    print("\n")
    
    # 错误的方式 - 使用 string
    try:
        parsed_json = json.loads(json_match.string)
        print("✅ 使用 json_match.string 成功:")
        print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"❌ 使用 json_match.string 失败: {e}")

else:
    print("没有找到JSON匹配")
