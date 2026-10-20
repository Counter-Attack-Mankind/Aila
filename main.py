
"""Minimal local console chat; no AstrBot dependency."""

import argparse
import os
from pathlib import Path

from aila.client import chat

ROOT = Path(__file__).resolve().parent


def load_persona():
    """加载 L1 核心人格与 L2 表达风格。"""
    persona_dir = ROOT / "persona"

    identity = (persona_dir / "identity.md").read_text(
        encoding="utf-8"
    )
    style = (persona_dir / "style.md").read_text(
        encoding="utf-8"
    )

    return identity + "\n\n" + style


def main():
    parser = argparse.ArgumentParser(description="艾拉 · 本地聊天")
    parser.add_argument(
        "--model",
        default=os.getenv("AILA_MODEL", "qwen3:8b")
    )
    parser.add_argument(
        "--endpoint",
        default=os.getenv(
            "AILA_OLLAMA_URL",
            "http://127.0.0.1:11434/api/chat"
        )
    )
    args = parser.parse_args()

    # 初始化人格与上下文
    persona = load_persona()
    history = [{"role": "system", "content": persona}]

    print(
        f"艾拉已启动（{args.model}）。"
        "输入 /exit 退出、/clear 清空上下文并重新加载人格。"
    )

    while True:
        try:
            message = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            break

        if not message:
            continue

        if message == "/exit":
            break

        if message == "/clear":
            # 重新读取最新的 L1 和 L2 人格文件
            persona = load_persona()
            history = [{"role": "system", "content": persona}]
            print("[上下文已清空，L1/L2 人格已重新加载]")
            continue

        candidate = history + [
            {"role": "user", "content": message}
        ]

        try:
            reply = chat(
                candidate,
                model=args.model,
                endpoint=args.endpoint
            )
        except (RuntimeError, KeyError, ValueError) as exc:
            print(f"[错误] {exc}")
            continue

        print(f"艾拉 > {reply}\n")

        history = candidate + [
            {"role": "assistant", "content": reply}
        ]

        # 保留 System Prompt 与最近 20 轮对话
        if len(history) > 41:
            history = [history[0]] + history[-40:]


if __name__ == "__main__":
    main()
