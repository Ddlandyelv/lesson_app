"""美术教案生成器 — 后端 API 服务"""

import os, sys, tempfile, json
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generator.ai_utils import generate_lesson, MODEL_CONFIGS
from generator.formatter import export
from generator.models import LessonData

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/models", methods=["GET"])
def get_models():
    result = {}
    for name, cfg in MODEL_CONFIGS.items():
        result[name] = {
            "model": cfg["model"],
            "vision": cfg["vision"],
            "note": cfg["note"],
            "api_url": cfg["api_url"],
        }
    return jsonify(result)

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    model_display = data.get("model", "通义千问 Qwen-VL (阿里云)")
    api_key = data.get("api_key", "")
    title = data.get("title", "")
    level = data.get("level", "")
    duration = data.get("duration", "")
    materials = data.get("materials", "")
    prompt = data.get("prompt", "")
    image_data = data.get("image_data", "")

    # 保存临时图片
    tmp_img_path = None
    if image_data:
        import base64
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img_bytes = base64.b64decode(image_data.split(",")[-1])
        tmp.write(img_bytes)
        tmp_img_path = tmp.name
        tmp.close()

    try:
        lesson = generate_lesson(
            model_display, api_key,
            title, level, duration, materials,
            prompt or "无额外要求",
            image_path=tmp_img_path,
        )

        result = {
            "success": True,
            "data": {
                "title": lesson.title,
                "level": lesson.level,
                "duration": lesson.duration,
                "materials": lesson.materials,
                "objectives": lesson.objectives,
                "key_points": lesson.key_points,
                "difficult_points": lesson.difficult_points,
                "process": lesson.process,
                "extension": lesson.extension,
                "notes": lesson.notes,
            },
        }
    except Exception as e:
        result = {"success": False, "error": str(e)}

    if tmp_img_path and os.path.exists(tmp_img_path):
        os.unlink(tmp_img_path)

    return jsonify(result)

@app.route("/api/download", methods=["POST"])
def download():
    data = request.get_json()
    fmt = data.get("format", "docx")
    image_data = data.get("image_data", "")

    # 保存临时图片
    tmp_img_path = None
    if image_data:
        import base64
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img_bytes = base64.b64decode(image_data.split(",")[-1])
        tmp.write(img_bytes)
        tmp_img_path = tmp.name
        tmp.close()

    lesson_data = LessonData(
        title=data.get("title", ""),
        level=data.get("level", ""),
        duration=data.get("duration", ""),
        materials=data.get("materials", ""),
        objectives=data.get("objectives", ""),
        key_points=data.get("key_points", ""),
        difficult_points=data.get("difficult_points", ""),
        process=data.get("process", ""),
        extension=data.get("extension", ""),
        notes=data.get("notes", ""),
    )

    output_dir = Path.home() / "Downloads"
    output_path = str(output_dir / f"教案文档.{'pdf' if fmt == 'pdf' else 'docx'}")

    export(lesson_data, output_path, fmt, image_path=tmp_img_path)

    if tmp_img_path and os.path.exists(tmp_img_path):
        os.unlink(tmp_img_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    import threading, time, webbrowser

    def _open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:5000")

    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5000)
