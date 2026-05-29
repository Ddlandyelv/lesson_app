"""API 连通性测试 — 验证密钥和模型是否可用"""

import os, sys, json
from openai import OpenAI

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API_KEY = input("请输入你的阿里云百炼 API 密钥: ").strip()
if not API_KEY:
    print("[FAIL] 密钥不能为空")
    sys.exit(1)

print()
print("=" * 50)
print("  测试阿里云百炼 API 连通性")
print("=" * 50)
print()

# 1. 测试基础文本对话
print(">>> 测试 1：基础文本对话 (qwen3.6-plus)")
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
try:
    resp = client.chat.completions.create(
        model="qwen3.6-plus",
        messages=[{"role": "user", "content": "用一句话介绍你自己"}],
        max_tokens=100,
    )
    content = resp.choices[0].message.content
    print(f"  [OK] 返回内容: {content[:100]}")
except Exception as e:
    print(f"  [FAIL] {str(e)[:200]}")
    print("  → 密钥无效、账户余额不足，或模型名不对")
    print()

# 2. 测试视觉模型（纯文本，不带图）
print(">>> 测试 2：视觉模型文本对话 (qwen3-vl-plus)")
try:
    resp = client.chat.completions.create(
        model="qwen3-vl-plus",
        messages=[{"role": "user", "content": "你支持图片识别吗？"}],
        max_tokens=100,
    )
    content = resp.choices[0].message.content
    print(f"  [OK] 返回内容: {content[:100]}")
except Exception as e:
    print(f"  [FAIL] {str(e)[:200]}")
    print()

# 3. 测试 JSON 输出
print(">>> 测试 3：JSON 格式输出")
try:
    resp = client.chat.completions.create(
        model="qwen3-vl-plus",
        messages=[
            {"role": "system", "content": "只输出纯 JSON，不要加任何其他文字：{\"name\": \"test\", \"value\": 123}"},
            {"role": "user", "content": "生成测试 JSON"},
        ],
        max_tokens=200,
    )
    content = resp.choices[0].message.content
    # 尝试解析 JSON
    data = json.loads(content)
    print(f"  [OK] JSON 解析成功: {data}")
except json.JSONDecodeError:
    print(f"  [FAIL] 返回内容不是有效 JSON: {content[:200]}")
except Exception as e:
    print(f"  [FAIL] {str(e)[:200]}")

print()
print("=" * 50)
print("  测试完成")
print("=" * 50)
