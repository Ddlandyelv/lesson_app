"""美术教案生成器 — 桌面版入口"""

import os
import sys
import subprocess
import threading
import time
import signal
import socket
import webview

APP_DIR = os.path.dirname(os.path.abspath(__file__))


def find_free_port():
    """找一个空闲端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_streamlit(port):
    """启动 Streamlit 服务"""
    cmd = [
        sys.executable,
        "-m", "streamlit", "run",
        os.path.join(APP_DIR, "app.py"),
        "--server.headless", "true",
        "--server.port", str(port),
        "--server.address", "127.0.0.1",
        "--browser.gatherUsageStats", "false",
        "--browser.serverPort", str(port),
    ]
    return subprocess.Popen(
        cmd,
        cwd=APP_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )


def main():
    port = find_free_port()

    # 启动 Streamlit
    proc = start_streamlit(port)
    time.sleep(3)

    # 创建本地窗口
    webview.create_window(
        title="美术教案生成器",
        url=f"http://127.0.0.1:{port}",
        width=1100,
        height=780,
        resizable=True,
        min_size=(800, 600),
        icon=os.path.join(APP_DIR, "icon.ico") if os.path.exists(os.path.join(APP_DIR, "icon.ico")) else None,
    )

    # 关闭窗口后清理
    proc.terminate()
    proc.wait()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"启动失败：{e}")
        input("按回车键退出...")
