"""专业文档排版 — HTML → PDF/DOCX"""

import os, base64, tempfile, re
from pathlib import Path
from .models import LessonData


def _build_html(data: LessonData, image_path=None) -> str:
    """生成排版精美的 HTML"""
    mats = data.materials or ""
    mat_list = [m.strip() for m in re.split(r"[,，、\\s]+", mats) if m.strip()]

    steps = []
    for s in (data.process or "").split("\n"):
        s = s.strip()
        if s:
            steps.append(s)

    img_tag = ""
    if image_path:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        img_tag = f'<div style="text-align:center;margin:20px 0;"><img src="data:image/png;base64,{b64}" style="max-width:100%;height:auto;max-height:300px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);" /></div>'

    mat_html = "".join(f'<span class="tag">{m}</span>' for m in mat_list)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
@page {{
  size: A4;
  margin: 2.5cm 2cm;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: '微软雅黑', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 12pt;
  line-height: 1.8;
  color: #1a1a1a;
  max-width: 720px;
  margin: 0 auto;
}}

h1 {{
  font-size: 22pt;
  text-align: center;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #c0a87a;
}}

.info {{ margin-bottom: 20px; }}
.info-item {{
  font-size: 11pt;
  color: #555;
  margin-bottom: 2px;
}}

h2 {{
  font-size: 16pt;
  font-weight: 700;
  color: #1a1a1a;
  margin-top: 28px;
  margin-bottom: 12px;
  padding-left: 12px;
  border-left: 4px solid #c0a87a;
}}

.body-text {{
  text-indent: 2em;
  margin-bottom: 8px;
  text-align: justify;
}}

.step {{ margin-bottom: 8px; }}
.step-title {{
  font-weight: 600;
  color: #333;
}}
.step-text {{
  text-indent: 2em;
  text-align: justify;
}}

.tag-row {{ margin: 8px 0; }}
.tag {{
  display: inline-block;
  background: #f5efe6;
  color: #a0724a;
  padding: 2px 14px;
  border-radius: 12px;
  margin: 3px 4px;
  font-size: 11pt;
}}

.label-text {{
  text-indent: 2em;
  margin-bottom: 4px;
}}

ul {{ padding-left: 2em; margin-bottom: 8px; }}
li {{ margin-bottom: 4px; text-align: justify; }}
</style>
</head>
<body>

<h1>《{_esc(data.title)}》教案</h1>

<div class="info">
  <div class="info-item">适用班级：{_esc(data.level or "（由教师填写）")}</div>
  <div class="info-item">课    时：{_esc(data.duration or "（由教师填写）")}</div>
  <div class="info-item">绘画材料：{_esc(data.materials or "（由教师填写）")}</div>
</div>

{img_tag}

<h2>一、教学目标</h2>
{_text_to_para(data.objectives)}

<h2>二、教学重难点</h2>
<p class="label-text">【教学重点】{_esc(data.key_points)}</p>
<p class="label-text">【教学难点】{_esc(data.difficult_points)}</p>

<h2>三、教学过程</h2>
{_steps_to_html(steps)}

<h2>四、所需材料</h2>
<div class="tag-row">{mat_html}</div>

{_optional_section("五、课后延伸", data.extension)}
{_optional_section("六、注意事项", data.notes, bullet=True)}

</body>
</html>"""
    return html


def _esc(text):
    text = str(text or "")
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _text_to_para(text):
    lines = [l.strip() for l in str(text or "").split("\n") if l.strip()]
    return "".join(f'<p class="body-text">{_esc(l)}</p>' for l in lines)


def _split_circled(text):
    """把包含 ①②③ 的文本按圈圈数字拆成多行"""
    import re
    parts = re.split(r"([①-⑩])", text)
    lines = []
    buf = ""
    for p in parts:
        if re.match(r"^[①-⑩]$", p):
            if buf.strip():
                lines.append(buf.strip())
            buf = p + " "
        else:
            buf += p
    if buf.strip():
        lines.append(buf.strip())
    return lines


def _steps_to_html(steps):
    html = ""
    for s in steps:
        if s.startswith("【"):
            # 分离标题和内容
            end = s.find("】")
            if end > 0:
                title = s[:end+1]
                content = s[end+1:].strip()
                html += f'<div class="step"><span class="step-title">{_esc(title)}</span></div>'
                if content:
                    sub_lines = _split_circled(content)
                    for sub in sub_lines:
                        html += f'<p class="step-text">{_esc(sub)}</p>'
            else:
                html += f'<div class="step"><span class="step-title">{_esc(s)}</span></div>'
        else:
            sub_lines = _split_circled(s)
            for sub in sub_lines:
                html += f'<p class="step-text">{_esc(sub)}</p>'
    return html


def _optional_section(title, content, bullet=False):
    if not content or not content.strip():
        return ""
    h = f"<h2>{title}</h2>"
    if bullet:
        items = [l.strip() for l in str(content).split("\n") if l.strip()]
        return h + "<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in items) + "</ul>"
    return h + f'<p class="body-text">{_esc(content)}</p>'


def export_docx(html: str, output_path: str):
    """HTML → DOCX（Word 可直接打开 HTML 保留格式）"""
    with open(output_path, "wb") as f:
        f.write(html.encode("utf-8"))


def export(data: LessonData, output_path: str, fmt: str = "docx", image_path=None):
    """统一导出"""
    from generator.template import LessonTemplate
    from generator.pdf_export import export_to_pdf

    if fmt == "pdf":
        export_to_pdf(data, output_path)
    else:
        html = _build_html(data, image_path)
        export_docx(html, output_path)
