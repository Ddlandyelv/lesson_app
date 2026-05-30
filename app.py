"""美术教案生成器 — Streamlit Web 界面"""

import streamlit as st
import os, tempfile
from pathlib import Path

from generator.models import LessonData
from generator.template import LessonTemplate
from generator.pdf_export import export_to_pdf
from generator.ai_utils import generate_lesson, MODEL_CONFIGS
from generator.key_store import save_key, load_keys, delete_key

st.set_page_config(
    page_title="美术教案生成器",
    page_icon="🎨",
    layout="centered",
    menu_items={"Get Help": None, "Report a Bug": None, "About": None},
)

# ── Open Design 风格样式 ──
st.markdown("""
<style>
:root {
  --bg: oklch(97.5% 0.006 65);
  --surface: oklch(100% 0 0);
  --fg: oklch(22% 0.025 35);
  --muted: oklch(48% 0.018 35);
  --border: oklch(89% 0.010 55);
  --accent: oklch(54% 0.16 35);
  --radius: 14px;
  --radius-sm: 8px;
}

.block-container { padding: 1rem 2rem 2rem !important; max-width: 880px !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stDeployButton"] { display: none !important; }
.stApp { background: var(--bg); }

/* 标题 */
h1 { font-weight: 600; color: var(--fg); letter-spacing: -0.02em; }
h1:first-of-type { font-size: 28px; margin-bottom: 4px; }
.stMarkdown p { font-size: 14px; color: var(--muted); margin-top: 4px; }

/* 侧边栏 */
section[data-testid="stSidebar"] {
  background: var(--surface);
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem; }
section[data-testid="stSidebar"] .stMarkdown h2 {
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.07em; color: var(--muted); margin: 0 0 12px;
}
section[data-testid="stSidebar"] hr { margin: 16px 0; border-color: var(--border); }

/* 输入框 */
.stTextInput>div>div>input, .stTextArea textarea {
  padding: 10px 14px !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  font-size: 14px !important;
  background: var(--bg) !important;
  color: var(--fg) !important;
  transition: border 0.15s, box-shadow 0.15s;
}
.stTextInput>div>div>input:focus, .stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px oklch(54% 0.16 35 / 0.12) !important;
}

/* 下拉框 */
.stSelectbox>div>div {
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
}
.stSelectbox>div>div:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px oklch(54% 0.16 35 / 0.12) !important;
}

/* 按钮 */
.stButton>button {
  background: linear-gradient(135deg, var(--accent), oklch(60% 0.18 28)) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 30px !important;
  padding: 12px 36px !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  box-shadow: 0 4px 18px oklch(54% 0.16 35 / 0.25) !important;
  transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton>button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 24px oklch(54% 0.16 35 / 0.32) !important;
}

/* 文件上传 */
.stFileUploader>div {
  border: 2px dashed var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 2rem !important;
  background: var(--surface) !important;
  transition: all 0.2s;
}
.stFileUploader>div:hover { border-color: var(--accent) !important; background: oklch(54% 0.16 35 / 0.03) !important; }

/* 提示框 */
.stAlert { border-radius: var(--radius-sm) !important; border: none !important; }

/* 进度条 */
.stProgress > div > div > div > div { background: var(--accent) !important; }

/* radio / checkbox */
.stRadio label, .stCheckbox label { font-size: 14px !important; }

/* caption */
.stCaption { font-size: 12px !important; color: var(--muted) !important; }

/* 分割线 */
hr { margin: 1rem 0; border: 0; border-top: 1px solid var(--border); }

/* 成功提示 */
.stSuccess { border-radius: var(--radius-sm) !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 美术教案生成器")
st.markdown("上传参考图片，AI 自动生成排版规范的教案文档。")

# ── 侧边栏 ──
with st.sidebar:
    st.header("⚙️ 设置")

    output_format = st.radio("输出格式", ["Word (.docx)", "PDF (.pdf)"], horizontal=True)
    st.divider()

    st.subheader("🤖 AI 模型")
    model_options = list(MODEL_CONFIGS.keys())
    model_display = st.selectbox("选择模型", model_options, index=0, label_visibility="collapsed")
    cfg = MODEL_CONFIGS[model_display]
    st.caption(f"模型名称：{cfg['model']}")
    st.caption(cfg['note'])
    st.markdown(f"[🔗 前往获取 API 密钥]({cfg['api_url']})")

    # 密钥
    saved_keys = load_keys()
    saved_api_key = saved_keys.get(model_display, "")

    if saved_api_key:
        api_key = st.text_input("API 密钥", type="password", value=saved_api_key)
        if st.button("清除已保存的密钥", use_container_width=True):
            delete_key(model_display)
            st.rerun()
        save_checked = False
    else:
        api_key = st.text_input("API 密钥", type="password", placeholder="输入 API 密钥……")
        save_checked = st.checkbox("记住此密钥，下次自动填入", value=True)

    st.divider()
    level = st.text_input("适用班级", placeholder="例：启蒙班、中级班")
    duration = st.text_input("课时", placeholder="例：45分钟")
    output_name = st.text_input("输出文件名", "教案文档")

# ── 主界面 ──
col1, col2 = st.columns([3, 2])
with col1:
    title = st.text_input("🎯 教案主题（选填）", placeholder="例：迎春花、蝴蝶，不填则 AI 自动识别")
    st.caption("不填的话 AI 会自动分析参考图片中的内容来确定主题")
    materials = st.text_area("🖌️ 绘画材料（选填）", placeholder="例：白卡纸、水粉颜料，不填则 AI 自动识别", height=80)
    st.caption("不填的话 AI 会根据图片中的作品判断使用材料")
    prompt = st.text_area("📝 创意提示词（选填）", placeholder="对教案内容的额外要求", height=100)

with col2:
    st.markdown("##### 🖼️ 参考图片（推荐必填）")
    uploaded_file = st.file_uploader("上传参考作品图片，AI 会分析其技法融入教案", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    st.markdown("##### ✏️ 手动编辑")
    edit_mode = st.toggle("生成后手动编辑内容", value=False)

# ── 生成 ──
if st.button("🚀 生成并下载", type="primary", use_container_width=True):
    if not api_key:
        st.error("请填写 API 密钥")
        st.stop()

    if not saved_api_key and save_checked:
        save_key(model_display, api_key)

    bar = st.progress(0, text="准备中……")

    try:
        tmp_img_path = None
        if uploaded_file:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            tmp.write(uploaded_file.getvalue())
            tmp_img_path = tmp.name
            tmp.close()

        bar.progress(20, text="📝 生成教案内容……")
        lesson_data = generate_lesson(model_display, api_key, title, level, duration, materials, prompt or "无额外要求", image_path=tmp_img_path)

        if lesson_data is None:
            st.error("AI 生成失败，请检查 API 密钥")
            st.stop()

        if edit_mode:
            st.divider()
            st.subheader("✏️ 编辑内容")
            lesson_data = LessonData(
                title=lesson_data.title,
                level=level,
                duration=duration,
                materials=lesson_data.materials,
                objectives=st.text_area("教学目标", lesson_data.objectives, height=100),
                key_points=st.text_area("教学重点", lesson_data.key_points, height=60),
                difficult_points=st.text_area("教学难点", lesson_data.difficult_points, height=60),
                process=st.text_area("教学过程", lesson_data.process, height=200),
                extension=st.text_area("课后延伸", lesson_data.extension, height=60),
                notes=st.text_area("注意事项", lesson_data.notes, height=80),
            )

        suffix = ".pdf" if output_format == "PDF (.pdf)" else ".docx"
        output_dir = Path.home() / "Downloads"
        base_path = output_dir / f"{output_name}{suffix}"
        out_path = str(base_path)
        c = 1
        while os.path.exists(out_path):
            try:
                open(out_path, "ab").close()
                break
            except OSError:
                out_path = str(output_dir / f"{output_name}_{c}{suffix}")
                c += 1

        bar.progress(70, text="📄 生成文档……")
        if output_format == "PDF (.pdf)":
            export_to_pdf(lesson_data, out_path)
        else:
            tmpl = LessonTemplate()
            tmpl.render(lesson_data, out_path, image_path=tmp_img_path)

        if tmp_img_path and os.path.exists(tmp_img_path):
            os.unlink(tmp_img_path)

        bar.progress(100, text="✅ 完成！")

        with open(out_path, "rb") as f:
            st.download_button(label=f"📥 下载 {os.path.basename(out_path)}", data=f, file_name=os.path.basename(out_path), use_container_width=True)
        st.success(f"已保存到：{out_path}")

    except Exception as e:
        st.error(f"生成失败：{str(e)}")

with st.expander("📖 使用说明"):
    st.markdown("""
    **基本流程**
    1. 左侧选择 AI 模型，填入 API 密钥（推荐通义千问，新用户有免费额度）
    2. 上传参考作品图片（推荐必填），AI 会分析其中的技法融入教案
    3. 填写教案主题和绘画材料（可不填，AI 自动从图片识别）
    4. 可选：填写创意提示词，告诉 AI 你想要的风格或方向
    5. 点击「生成并下载」

    **输出格式**
    - **Word (.docx)：** 排版规范的教案文档，可打印或二次编辑
    - **PDF (.pdf)：** 适合直接发送或打印

    **AI 模型说明**
    | 模型 | 看图 | 费用 |
    |------|:----:|------|
    | 通义千问 Qwen-VL (阿里云) | ✅ | 新用户 7000 万免费 tokens |
    | GLM-5V-Turbo (智谱AI) | ✅ | 新用户有免费额度 |
    | 小米 MiMo-VL | ✅ | 按量付费 |
    | Kimi-VL (月之暗面) | ✅ | 按量付费，8K 版 ¥2/百万 tokens |

    **记住密钥**
    - 勾选「记住此密钥」后，下次打开页面自动填入，不用重复粘贴
    - 每个模型的密钥独立保存，互不影响
    - 点击「清除已保存的密钥」可删除

    **常见问题**
    - **API 密钥在哪获取？** 点击模型名称旁的「获取密钥」链接跳转官网
    - **生成失败？** 检查密钥是否有效、余额是否充足、模型是否已开通
    - **主题/材料不填可以吗？** 可以，AI 会从上传的图片中自动识别
    """)

st.caption("支持 Word / PDF 导出")
