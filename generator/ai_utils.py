"""AI 内容生成模块 - 多模型支持"""

import json
import os
from typing import Optional
from .models import LessonData

# 模型配置
MODEL_CONFIGS = {
    "通义千问 Qwen-VL (阿里云)": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen3-vl-plus",
        "vision": True,
        "note": "有免费额度，支持看图，推荐",
        "api_url": "https://bailian.console.aliyun.com",
    },
    "GLM-5V-Turbo (智谱AI)": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-5v-turbo",
        "vision": True,
        "note": "最新多模态Coding基座，200K上下文",
        "api_url": "https://open.bigmodel.cn",
    },
    "小米 MiMo-VL": {
        "base_url": "https://api.xiaomimimo.com/v1",
        "model": "xiaomi/mimo-v2.5",
        "vision": True,
        "note": "原生全模态，支持图片/视频/音频",
        "api_url": "https://platform.xiaomimimo.com",
    },
    "Kimi-VL (月之暗面)": {
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k-vision-preview",
        "vision": True,
        "note": "支持看图，8K版 ¥2/百万tokens",
        "api_url": "https://platform.moonshot.cn",
    },
}

SYSTEM_PROMPT = """你是一位经验丰富的美术教案编写专家。根据用户提供的主题和要求，生成一份结构完整的教案。
只输出纯 JSON，不要加任何 Markdown 标记、代码块、注释或说明文字。

JSON 格式：{
  "title": "从图片或用户输入中识别的教案主题",
  "materials": "从图片或用户输入中识别的绘画材料清单",
  "objectives": "教学目标，从知识技能、过程方法、情感态度三个维度写，每行一个维度，用【】标记",
  "key_points": "教学重点",
  "difficult_points": "教学难点",
  "process": "教学过程，分步骤写，每步用【步骤一】之类的标题开头，包含教师示范、学生练习、巡回指导等环节",
  "extension": "课后延伸",
  "notes": "注意事项，每行一条"
}

要求：
- 如果用户提供了主题，title 填用户提供的值；如果没提供，从图片内容识别主题并填入
- 如果用户提供了材料，materials 填用户提供的值；如果没提供，根据图片中的作品判断材料并填入
- 教学目标要具体可操作，不要空泛
- 教学过程要详细，包含具体的技法指导步骤
- 如果用户上传了参考图片，分析图片中的构图、色彩、技法、风格，并融入教案内容"""


def _detect_mime(file_path: str) -> str:
    """根据文件后缀返回正确的 MIME 类型"""
    ext = os.path.splitext(file_path)[1].lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }.get(ext, "image/png")


def _parse_json_response(content) -> dict:
    # 强制转字符串
    if not isinstance(content, str):
        content = str(content)
    content = content.strip()

    # 去掉 markdown 代码块标记
    if "```" in content:
        # 取最后一个 ``` 之前的内容
        parts = content.split("```")
        for part in parts:
            part = part.strip()
            # 去掉开头的语言标记（如 json）
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{") or part.startswith("["):
                content = part
                break

    # 尝试提取 JSON 对象（{...}）
    first_brace = content.find("{")
    last_brace = content.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        content = content[first_brace : last_brace + 1]

    # 尝试解析
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # 如果失败，尝试修复常见问题再解析
        # 替换单引号为双引号
        fixed = content.replace("'", '"')
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            # 如果仍然失败，抛出异常并附带返回内容片段
            snippet = content[:200] + "..." if len(content) > 200 else content
            raise RuntimeError(
                f"AI 返回的内容无法解析为 JSON。\n"
                f"请检查 API 密钥是否有效、模型是否支持、账户余额是否充足。\n"
                f"返回内容：{snippet}"
            )


def _ensure_str(val):
    """将列表转成换行分隔的字符串，防止 AI 返回数组格式"""
    if isinstance(val, list):
        return "\n".join(str(x) for x in val)
    if val is None:
        return ""
    return str(val)


def _build_lesson(data: dict, title: str, level: str, duration: str, materials: str) -> LessonData:
    # 如果用户没填主题或材料，从 AI 返回的 JSON 中提取
    final_title = title if title.strip() else _ensure_str(data.get("title", ""))
    final_materials = materials if materials.strip() else _ensure_str(data.get("materials", ""))
    return LessonData(
        title=final_title,
        level=level,
        duration=duration,
        materials=final_materials,
        objectives=_ensure_str(data.get("objectives", "")),
        key_points=_ensure_str(data.get("key_points", "")),
        difficult_points=_ensure_str(data.get("difficult_points", "")),
        process=_ensure_str(data.get("process", "")),
        extension=_ensure_str(data.get("extension", "")),
        notes=_ensure_str(data.get("notes", "")),
    )


def _build_text(title: str, level: str, duration: str, materials: str, prompt: str, has_image: bool) -> str:
    text = "请生成一份教案。\n\n"

    if title.strip():
        text += f"主题：{title}\n"
    else:
        text += "主题：请从图片中识别主题并填入\n"

    text += f"适用班级：{level}\n"
    text += f"课时：{duration}\n"

    if materials.strip():
        text += f"绘画材料：{materials}"
    else:
        text += "绘画材料：请从图片中判断所用材料并填入"

    if has_image:
        text += "\n\n【参考图片】用户上传了参考作品图片，请分析图片中的构图、色彩运用、绘画技法、风格特点，并将分析结果融入教案的教学目标和过程中。"

    if prompt:
        text += f"\n\n额外要求：{prompt}"

    return text


def _call_openai_compatible(
    api_key: str, base_url: str, model: str, text: str, image_path: Optional[str] = None
) -> str:
    """调用 OpenAI 兼容接口"""
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)

    if image_path:
        import base64

        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        mime = _detect_mime(image_path)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
                ],
            },
        ]
    else:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ]

    response = client.chat.completions.create(
        model=model,
        max_tokens=4000,
        temperature=0.7,
        messages=messages,
    )

    msg = response.choices[0].message
    # 国产模型返回格式不一：content 可能是 str / list / None
    if msg.content and isinstance(msg.content, str):
        return msg.content
    # 尝试从其他字段取内容
    if hasattr(msg, "content") and msg.content is not None:
        return str(msg.content)
    # 兜底：尝试序列化
    try:
        return msg.model_dump_json()
    except Exception:
        return str(msg)


def generate_lesson(
    model_display: str,
    api_key: str,
    title: str,
    level: str,
    duration: str,
    materials: str,
    prompt: str,
    image_path: Optional[str] = None,
) -> Optional[LessonData]:
    if not api_key:
        return None

    config = MODEL_CONFIGS.get(model_display)
    if not config:
        raise RuntimeError(f"未知模型：{model_display}")

    supports_vision = config.get("vision", False)
    has_image = bool(image_path and supports_vision)
    text = _build_text(title, level, duration, materials, prompt, has_image)

    img_path = image_path if supports_vision else None

    try:
        raw = _call_openai_compatible(
            api_key, config["base_url"], config["model"], text, img_path
        )
        data = _parse_json_response(raw)
        return _build_lesson(data, title, level, duration, materials)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"AI 返回的格式无法解析。\n"
            f"可能原因：API 密钥无效、模型不支持、或账户余额不足。\n"
            f"错误详情：{str(e)}"
        )
    except Exception as e:
        raise RuntimeError(f"AI 生成失败（{model_display}）：{str(e)}")
