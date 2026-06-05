
<div align="center">
  <h1>🎨 美术教案生成器</h1>
  <p>上传参考作品图片，AI 自动生成一份排版规范的教案文档</p>
  <p>
    <a href="#-快速开始">快速开始</a> ·
    <a href="#-功能">功能</a> ·
    <a href="#-使用方式">使用方式</a> ·
    <a href="#-项目结构">项目结构</a>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue" />
    <img src="https://img.shields.io/badge/License-MIT-green" />
    <img src="https://img.shields.io/badge/Flask-3.0-lightgrey" />
  </p>
</div>

<br />

![应用截图](examples/screenshot.png)

## 📋 功能

- **AI 自动生成教案** — 支持通义千问 Qwen-VL、GLM-5V-Turbo、小米 MiMo-VL、Kimi-VL
- **图片分析** — AI 自动分析参考作品的构图、色彩、技法并融入教案
- **双格式导出** — Word (.docx) 和 PDF (.pdf) 两种输出格式
- **专业排版** — HTML+CSS 排版引擎，自动处理步骤编号、材料标签、参考图嵌入
- **自动识别** — 主题和材料可不填，AI 自动从图片识别
- **记住密钥** — 每个模型的 API 密钥独立本地保存
- **双模式** — Web 界面和命令行两种交互方式

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 后端 API | [Flask](https://flask.palletsprojects.com/) |
| 前端界面 | 纯 HTML + CSS + JS（Open Design 设计） |
| AI 调用 | [OpenAI SDK](https://github.com/openai/openai-python)（兼容国产模型） |
| 文档排版 | HTML → DOCX 专业 CSS 排版 + [fpdf2](https://pyfpdf.github.io/fpdf2/) PDF 输出 |
| 图片处理 | [Pillow](https://python-pillow.org/) |

## 🚀 快速开始

### Windows 一键启动（推荐）

下载项目后，**双击 `一键启动教案生成器.bat`**，自动打开浏览器进入教案生成页面。

### 手动启动

```bash
# 1. 进入项目
cd lesson_app

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python server.py

# 4. 打开浏览器访问
# http://localhost:5000
```

## 📖 使用方式

### Web 界面（推荐）

打开 `http://localhost:5000` 即可使用。

1. 左侧选择 AI 模型 → 填入 API 密钥
2. 上传参考作品图片
3. 填写主题和材料（可选，AI 自动识别）
4. 点击「生成教案」
5. 预览结果后点击「下载教案文档」

### 命令行版

```bash
python cli.py
```

### 诊断工具

```bash
python diagnose.py
```

### Streamlit 版（旧版）

```bash
streamlit run app.py
```

### 支持的 AI 模型

| 模型 | 看图 | 免费额度 | 网络 |
|------|:----:|---------|:----:|
| 通义千问 Qwen-VL (阿里云) | ✅ | 新用户 7000 万 tokens | 直连 |
| GLM-5V-Turbo (智谱AI) | ✅ | 新用户有免费额度 | 直连 |
| 小米 MiMo-VL | ✅ | 按量付费 | 直连 |
| Kimi-VL (月之暗面) | ✅ | 按量付费 ¥2/百万tokens | 直连 |

## 📁 项目结构

```
lesson_app/
├── server.py              # Flask 后端 API（主入口）
├── index.html             # Open Design 前端界面
├── 一键启动教案生成器.bat   # Windows 双击启动
├── app.py                 # Streamlit 版本（备用）
├── cli.py                 # 命令行版本
├── diagnose.py            # 诊断工具
├── requirements.txt
├── CHANGELOG.md           # 更新日志
├── generator/
│   ├── ai_utils.py        # AI 调用与模型配置
│   ├── formatter.py       # HTML 专业排版引擎
│   ├── template.py        # Word 排版（python-docx）
│   ├── pdf_export.py      # PDF 排版（fpdf2）
│   ├── models.py          # 数据结构
│   └── key_store.py       # 本地密钥存储
├── examples/              # 样例输出
│   ├── 迎春花教案样例.docx
│   ├── 迎春花教案样例.pdf
│   └── screenshot.png
└── .streamlit/
    └── config.toml
```

## 📄 输出样例

[examples/迎春花教案样例.docx](examples/迎春花教案样例.docx) · [examples/迎春花教案样例.pdf](examples/迎春花教案样例.pdf)

## ⚙️ 工作原理

```
上传图片 + 填写信息 → Flask API → AI 模型分析 → HTML 排版 → 输出 Word/PDF
```

## 📝 注意事项

- API 密钥仅在当前会话使用，不会上传
- 首次使用建议开通阿里云百炼免费额度

## 📄 许可证

MIT
