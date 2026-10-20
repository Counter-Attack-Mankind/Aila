
"""Aila - Local console chat."""

import argparse
import os
from pathlib import Path

from aila.client import chat
from aila.identity import (
    resolve_identity,
    identity_context,
    guard_reply,
)
from aila.knowledge import build_knowledge_context

ROOT = Path(__file__).resolve().parent


def load_persona():
    """Load L1 identity and L2 expression style."""
    persona_dir = ROOT / "persona"

    identity = (persona_dir / "identity.md").read_text(
        encoding="utf-8"
    )
    style = (persona_dir / "style.md").read_text(
        encoding="utf-8"
    )

    return identity + "\n\n" + style


def main():
    parser = argparse.ArgumentParser(
        description="艾拉 · 本地聊天"
    )
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

    # --------------------------------------------------
    # 1. Load persona
    # --------------------------------------------------
    persona = load_persona()

    # --------------------------------------------------
    # 2. Resolve trusted session identity
    # Console defaults to guest.
    # Never authenticate through message content.
    # --------------------------------------------------
    identity = resolve_identity(platform="console")

    # --------------------------------------------------
    # 3. Initialize conversation history
    # --------------------------------------------------
    history = [
        {"role": "system", "content": persona}
    ]

    debug = False
    last_topic = None

    print(
        f"艾拉已启动（{args.model}）。"
        "输入 /exit 退出、/clear 清空、"
        "/debug 切换调试。"
    )
    print(f"[会话身份] {identity.role}")

    while True:
        try:
            message = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            break

        if not message:
            continue

        # --------------------------------------------------
        # Commands
        # --------------------------------------------------
        if message == "/exit":
            break

        if message == "/clear":
            persona = load_persona()

            history = [
                {"role": "system", "content": persona}
            ]

            last_topic = None

            # Re-resolve trusted identity, not user claims.
            identity = resolve_identity(
                platform="console"
            )

            print("[上下文已清空，人格已重新加载]")
            print(f"[会话身份] {identity.role}")
            continue

        if message == "/debug":
            debug = not debug
            print(
                f"[知识调试：{'开' if debug else '关'}]"
            )
            continue

        # --------------------------------------------------
        # 4. Retrieve knowledge for this turn
        # --------------------------------------------------
        context, topic = build_knowledge_context(
            message,
            last_topic=last_topic,
        )

        if debug:
            print(f"[会话身份] {identity.role}")
            print(
                f"[知识命中] {topic if topic else '无'}"
            )
            if context:
                print(f"[知识内容]\n{context}")

        # --------------------------------------------------
        # 5. Build model input
        # Identity and knowledge are temporary context.
        # They are NOT stored as conversation history.
        # --------------------------------------------------
        candidate = history.copy()

        candidate.append({
            "role": "system",
            "content": identity_context(identity),
        })

        if context:
            candidate.append({
                "role": "system",
                "content": context,
            })

        candidate.append({
            "role": "user",
            "content": message,
        })

        # --------------------------------------------------
        # 6. Generate response
        # --------------------------------------------------
        try:
            reply = chat(
                candidate,
                model=args.model,
                endpoint=args.endpoint,
            )
        except (
            RuntimeError,
            KeyError,
            ValueError,
        ) as exc:
            print(f"[错误] {exc}")
            continue

        # --------------------------------------------------
        # 7. Apply identity protection
        # --------------------------------------------------
        reply = guard_reply(reply, identity)

        print(f"艾拉 > {reply}\n")

        # --------------------------------------------------
        # 8. Save real conversation only
        # --------------------------------------------------
        history.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": reply},
        ])

        # Retain system prompt and last 20 turns.
        if len(history) > 41:
            history = [history[0]] + history[-40:]

        # Update the last successfully retrieved topic.
        if topic:
            last_topic = topic


if __name__ == "__main__":
    main()
