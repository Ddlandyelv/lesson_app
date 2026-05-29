#!/usr/bin/env python3
"""美术教案生成器 — 终端命令行版"""

import os, sys, tempfile, time, json
from pathlib import Path
from generator.ai_utils import generate_lesson, MODEL_CONFIGS
from generator.template import LessonTemplate
from generator.pdf_export import export_to_pdf

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def c(text, color=""):
    """带颜色输出"""
    colors = {"green": "32", "blue": "34", "yellow": "33", "red": "31", "cyan": "36", "gray": "90"}
    ccode = colors.get(color, "")
    if ccode:
        print(f"\033[{ccode}m{text}\033[0m")
    else:
        print(text)


def ask(prompt, default=""):
    """带提示色的输入"""
    c(f"\n┃ {prompt}", "cyan")
    if default:
        c(f"┃ 留空则: {default}", "gray")
    val = input("┗> ").strip()
    return val


def step(msg):
    """输出步骤分隔"""
    c(f"\n{'='*50}", "blue")
    c(f"  {msg}", "blue")
    c(f"{'='*50}", "blue")


def log(msg, status="⏳"):
    c(f"  {status} {msg}", "green" if status == "✅" else "gray")


def main():
    c(r"""
    ╔═══════════════════════════╗
    ║   美术教案生成器           ║
    ╚═══════════════════════════╝
    """, "cyan")

    # 模型选择
    step("第一步：配置模型")
    models = list(MODEL_CONFIGS.keys())
    for i, name in enumerate(models, 1):
        cfg = MODEL_CONFIGS[name]
        vision = "🖼️ 支持看图" if cfg["vision"] else "📝 纯文本"
        c(f"  [{i}] {name}  {vision}  {cfg['note']}", "gray")

    try:
        choice = int(ask("请输入编号", f"默认 1: {models[0]}") or "1")
        sel_model = models[choice - 1]
    except (ValueError, IndexError):
        sel_model = models[0]
    c(f"  → 已选: {sel_model}", "green")

    cfg = MODEL_CONFIGS[sel_model]
    c(f"  → 官网: {cfg['api_url']}", "gray")

    api_key = ask("请输入 API 密钥", "粘贴你的密钥")
    if not api_key:
        c("  ❌ 密钥不能为空", "red")
        return

    # 输出格式
    c(f"\n┃ 输出格式", "cyan")
    c("  [1] Word (.docx)", "gray")
    c("  [2] PDF (.pdf)", "gray")
    fmt_choice = ask("请输入编号", "默认 1") or "1"
    out_format = "PDF (.pdf)" if fmt_choice == "2" else "Word (.docx)"
    c(f"  → 已选: {out_format}", "green")

    # 图片
    step("第二步：上传参考图片")
    c("  请将图片路径粘贴到下面", "yellow")
    img_path = ask("图片路径", "如 C:/Users/.../图片.jpg")
    if img_path:
        img_path = img_path.strip('"').strip("'")
        if not os.path.exists(img_path):
            c(f"  ❌ 文件不存在: {img_path}", "red")
            img_path = None
        else:
            c(f"  ✅ 已读取: {os.path.basename(img_path)}", "green")
    else:
        c("  ⚠️ 未上传图片，AI 将无法分析参考作品", "yellow")

    # 信息填写
    step("第三步：填写基本信息（均可留空）")
    title = ask("教案主题", "不填则 AI 自动识别")
    level = ask("适用班级", "如：启蒙班")
    duration = ask("课时", "如：45分钟")
    materials = ask("绘画材料", "不填则 AI 自动识别")
    prompt = ask("创意提示词", "对教案的额外要求，可留空")

    # 生成
    step("第四步：正在生成")
    log(f"模型: {sel_model}")
    log(f"API密钥: {api_key[:8]}...{api_key[-4:]}")

    try:
        log("正在调用 AI 生成教案内容……")
        lesson = generate_lesson(sel_model, api_key, title, level, duration, materials, prompt or "无额外要求", image_path=img_path or None)
        log("AI 返回成功，正在解析", "✅")

        log("正在生成文档……")
        suffix = ".pdf" if out_format == "PDF (.pdf)" else ".docx"
        output_name = "教案文档"
        output_dir = Path.home() / "Downloads"
        out_path = str(output_dir / f"{output_name}{suffix}")

        counter = 1
        while os.path.exists(out_path):
            try:
                open(out_path, "ab").close()
                break
            except OSError:
                out_path = str(output_dir / f"{output_name}_{counter}{suffix}")
                counter += 1

        if out_format == "PDF (.pdf)":
            export_to_pdf(lesson, out_path)
        else:
            tmpl = LessonTemplate()
            tmpl.render(lesson, out_path, image_path=img_path or None)

        log(f"{out_format} 已生成: {out_path}", "✅")
        c(f"\n{'='*50}", "green")
        c(f"  ✅ 教案生成完成！", "green")
        c(f"  文件: {out_path}", "green")
        c(f"{'='*50}", "green")

    except Exception as e:
        c(f"\n  ❌ 生成失败: {str(e)}", "red")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        c("\n\n  ⚠️ 已取消", "yellow")
    except Exception as e:
        c(f"\n  ❌ 错误: {str(e)}", "red")
