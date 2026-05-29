"""项目诊断工具 — 运行该脚本检查项目是否正常"""

import sys
import os
import socket
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def check(label, ok, detail=""):
    mark = "[OK]" if ok else "[FAIL]"
    print(f"  {mark} {label}")
    if detail:
        print(f"       {detail}")
    return ok


def main():
    print("=" * 50)
    print("  美术教案生成器 - 项目诊断")
    print("=" * 50)
    print()

    all_ok = True

    # 1. 项目结构
    print(">>> 项目结构")
    required = ["app.py", "requirements.txt",
                 "generator/__init__.py", "generator/models.py",
                 "generator/template.py", "generator/ai_utils.py",
                 "generator/pdf_export.py"]
    for path in required:
        exists = (ROOT / path).exists()
        all_ok &= check(f"  {path}", exists)
    print()

    # 2. Python 版本
    print(">>> Python 环境")
    py_ok = sys.version_info >= (3, 9)
    all_ok &= check(f"  Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", py_ok, "需要 >= 3.9")
    print()

    # 3. 依赖检查
    print(">>> 依赖检查")
    deps = {"streamlit": "streamlit", "openai": "openai", "fpdf2": "fpdf",
            "Pillow": "PIL", "python-docx": "docx"}
    for name, import_name in deps.items():
        try:
            __import__(import_name)
            check(f"  {name}", True)
        except ImportError as e:
            all_ok &= check(f"  {name}", False, str(e))
    print()

    # 4. 模块导入
    print(">>> 模块导入")
    try:
        from generator.models import LessonData
        check("  models.LessonData", True)
    except Exception as e:
        all_ok &= check("  models.LessonData", False, str(e))

    try:
        from generator.template import LessonTemplate
        check("  template.LessonTemplate", True)
    except Exception as e:
        all_ok &= check("  template.LessonTemplate", False, str(e))

    try:
        from generator.ai_utils import MODEL_CONFIGS, _detect_mime
        check("  ai_utils", True)
        for name in MODEL_CONFIGS:
            cfg = MODEL_CONFIGS[name]
            check(f"    - {name} | model={cfg['model']}", True)
    except Exception as e:
        all_ok &= check("  ai_utils", False, str(e))

    try:
        from generator.pdf_export import export_to_pdf
        check("  pdf_export.export_to_pdf", True)
    except Exception as e:
        all_ok &= check("  pdf_export.export_to_pdf", False, str(e))
    print()

    # 5. 端口检查
    print(">>> 端口状态")
    found_port = False
    for port in range(8501, 8520):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        if result == 0:
            try:
                resp = urllib.request.urlopen(f"http://127.0.0.1:{port}", timeout=2)
                check(f"  端口 {port}", True, f"HTTP {resp.status}")
                found_port = True
            except Exception:
                pass
    if not found_port:
        print("  (没有运行中的实例)")
    print()

    # 6. PDF 字体检查
    print(">>> PDF 字体")
    fonts = ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc",
             "C:/Windows/Fonts/simsun.ttc"]
    for f in fonts:
        all_ok &= check(f"  {Path(f).name}", Path(f).exists())
    print()

    # 汇总
    print("=" * 50)
    if all_ok:
        print("  诊断通过 - 项目可以运行")
    else:
        print("  存在问题 - 请根据上方提示修复")
    print("=" * 50)


if __name__ == "__main__":
    main()
