"""本地 API 密钥存储"""

import json, os
from pathlib import Path

KEYS_FILE = Path(__file__).resolve().parent.parent / "api_keys.json"


def load_keys() -> dict:
    """读取本地存储的 API 密钥"""
    if KEYS_FILE.exists():
        try:
            return json.loads(KEYS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_key(model_name: str, api_key: str):
    """保存某个模型的 API 密钥"""
    keys = load_keys()
    keys[model_name] = api_key
    KEYS_FILE.write_text(json.dumps(keys, ensure_ascii=False, indent=2), encoding="utf-8")


def get_key(model_name: str) -> str:
    """获取某个模型的 API 密钥"""
    return load_keys().get(model_name, "")


def delete_key(model_name: str):
    """删除某个模型的 API 密钥"""
    keys = load_keys()
    keys.pop(model_name, None)
    KEYS_FILE.write_text(json.dumps(keys, ensure_ascii=False, indent=2), encoding="utf-8")
