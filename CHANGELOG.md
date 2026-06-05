# 更新日志

## v1.1.1 (2026-05-29)

### 新增

- **一键启动脚本**：新增 `一键启动教案生成器.bat`，Windows 用户双击即启动
- 更新 README 添加一键启动说明

## v1.1.0 (2026-05-30)

### 完整重构：Open Design 前端 + Flask 后端 + HTML 排版引擎

美术教案生成器 — 上传美术作品图片，AI 自动生成排版规范的教案文档。

### 功能

- **AI 教案生成**：支持通义千问 Qwen-VL、GLM-5V-Turbo、小米 MiMo-VL、Kimi-VL 四种模型
- **图片分析**：AI 自动分析参考作品的构图、色彩、技法并融入教案内容
- **双格式导出**：Word (.docx) 和 PDF (.pdf) 两种输出格式
- **HTML+CSS 专业排版**：22pt 居中标题加金色装饰线、16pt 小节标题加左侧竖线、12pt 微软雅黑正文、首行缩进两端对齐
- **步骤竖向排列**：教学步骤中的圆圈数字（①②③）自动拆分为独立行
- **参考图嵌入**：生成的文档中自动包含上传的参考图片（圆角阴影居中展示）
- **自动识别**：教案主题和材料可不填，AI 自动从图片识别
- **记住密钥**：每个模型的 API 密钥独立本地保存，下次自动填入
- **双模式运行**：Web 界面（Flask + HTML）和命令行（cli.py）
- **诊断工具**：内置 diagnose.py 一键检查项目状态

### 界面

- 基于 Open Design 生成的温暖干净 UI
- OKLCH 色彩系统，暖金色点缀
- 侧边栏可收起，移动端响应式适配
- 拖拽上传图片，实时预览
- 折叠式使用说明
- 生成结果可复制、可编辑、可重新生成

### 技术栈

- 后端：Flask (Python)
- 前端：纯 HTML + CSS + JS（无框架）
- AI 调用：OpenAI 兼容 SDK
- 文档生成：HTML → DOCX（Word 可直接打开），fpdf2 → PDF
- 排版引擎：generator/formatter.py（HTML + CSS 专业排版）

### 文件结构

```
lesson_app/
├── app.py                 # Streamlit 版本（保留）
├── server.py              # Flask 后端 API 服务
├── index.html             # Open Design 前端界面
├── cli.py                 # 命令行版本
├── diagnose.py            # 诊断工具
├── CHANGELOG.md           # 更新日志
├── README.md              # 项目说明
├── requirements.txt       # 依赖清单
├── pyproject.toml         # 项目配置
├── .gitignore             # Git 忽略规则
├── LICENSE                # MIT 协议
├── generator/
│   ├── ai_utils.py        # AI 模型调用与配置
│   ├── formatter.py       # 文档排版引擎 (HTML→DOCX/PDF)
│   ├── template.py        # Word 排版（python-docx）
│   ├── pdf_export.py      # PDF 排版（fpdf2）
│   ├── models.py          # 数据结构
│   ├── key_store.py       # 本地密钥存储
│   └── excel_export.py    # Excel 导出（旧版保留）
├── examples/
│   ├── 迎春花教案样例.docx
│   ├── 迎春花教案样例.pdf
│   └── screenshot.png
└── .streamlit/
    └── config.toml
```
