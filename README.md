
<div align="center">
  <h1>🎨 美术教案生成器</h1>
  <p>上传参考作品图片，AI 自动生成一份排版规范的教案文档</p>
  <p>
    <a href="#-在线使用">在线使用</a> ·
    <a href="#-本地运行">本地运行</a> ·
    <a href="#-功能">功能</a> ·
    <a href="#-使用说明">使用说明</a> ·
    <a href="#-项目结构">项目结构</a>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue" />
    <img src="https://img.shields.io/badge/License-MIT-green" />
    <img src="https://img.shields.io/badge/Flask-3.0-lightgrey" />
    <img src="https://img.shields.io/badge/Mobile-Responsive-orange" />
  </p>
</div>

<br />

![应用截图](examples/screenshot.png)

## 🌐 在线使用（推荐）

**直接打开即用，无需安装：**

👉 **[https://ddlyl.pythonanywhere.com](https://ddlyl.pythonanywhere.com)**

电脑和手机都能用，页面自动适配。

---

## 💻 本地运行

### Windows 一键启动

下载项目后，**双击 `一键启动教案生成器.bat`**，自动打开浏览器。

### 手动启动

```bash
# 1. 进入项目
cd lesson_app

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python server.py

# 4. 打开浏览器访问 http://localhost:5000
```

---

## 📋 功能

- **AI 自动生成教案** — 支持通义千问 Qwen-VL、GLM-5V-Turbo、小米 MiMo-VL、Kimi-VL
- **手机端适配** — 响应式设计，手机浏览器打开直接使用
- **图片分析** — AI 自动分析参考作品的构图、色彩、技法并融入教案
- **双格式导出** — Word (.docx) 和 PDF (.pdf) 两种输出格式
- **专业排版** — HTML+CSS 排版引擎，自动处理步骤编号、材料标签、参考图嵌入
- **自动识别** — 主题和材料可不填，AI 自动从图片识别
- **记住密钥** — API 密钥存储在本地浏览器中，安全不泄露

---

## 📖 使用说明

### 1. 选择模型

展开「模型与设置」面板，选择 AI 模型（推荐通义千问），填入对应的 API 密钥。

### 2. 上传作品

手机点击上传区域 → 拍照或从相册选择学生作品图片。

### 3. 填写信息（可选）

教案主题、材料、班级、课时都可以不填，AI 会根据图片自动识别。

### 4. 生成教案

点击底部「生成教案」按钮，等待 AI 完成。

### 5. 下载文件

生成后点击「下载教案文档」，选择 Word 或 PDF 格式保存。

---

### 支持的 AI 模型

| 模型 | 看图 | 免费额度 | 获取密钥 |
|------|:----:|---------|------|
| 通义千问 Qwen-VL (阿里云) | ✅ | 新用户 7000 万 tokens | [百炼平台](https://bailian.console.aliyun.com) |
| GLM-5V-Turbo (智谱AI) | ✅ | 新用户有免费额度 | [智谱开放平台](https://open.bigmodel.cn) |
| 小米 MiMo-VL | ✅ | 按量付费 | [小米平台](https://platform.xiaomimimo.com) |
| Kimi-VL (月之暗面) | ✅ | ¥2/百万tokens | [Moonshot](https://platform.moonshot.cn) |

### 命令行版

```bash
python cli.py
```

### 诊断工具

```bash
python diagnose.py
```

---

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 后端 API | [Flask](https://flask.palletsprojects.com/) |
| 前端界面 | 纯 HTML + CSS + JS（Open Design 移动端适配） |
| AI 调用 | [OpenAI SDK](https://github.com/openai/openai-python)（兼容国产模型） |
| 文档排版 | HTML → DOCX 专业 CSS 排版 + [fpdf2](https://pyfpdf.github.io/fpdf2/) PDF 输出 |
| 图片处理 | [Pillow](https://python-pillow.org/) |
| 部署 | [PythonAnywhere](https://www.pythonanywhere.com) 免费托管 |

---

## 📁 项目结构

```
lesson_app/
├── server.py              # Flask 后端 API（主入口）
├── index.html             # 移动端适配前端界面
├── 一键启动教案生成器.bat   # Windows 双击启动
├── app.py                 # Streamlit 版本（备用）
├── cli.py                 # 命令行版本
├── diagnose.py            # 诊断工具
├── requirements.txt       # Python 依赖
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

- API 密钥存储在浏览器本地，不会上传到服务器
- 首次使用建议开通阿里云百炼免费额度
- 在线版为免费托管，15 分钟无访问可能自动休眠，刷新即恢复

## 📄 许可证

MIT
