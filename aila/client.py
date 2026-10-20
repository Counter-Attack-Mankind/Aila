"""Small, platform-independent Ollama client."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def chat(messages, model="qwen3:8b", endpoint="http://127.0.0.1:11434/api/chat"):
    payload = json.dumps({
        "model": model, "messages": messages, "stream": False, "think": False,
        "options": {"temperature": 0.7},
    }, ensure_ascii=False).encode("utf-8")
    req = Request(endpoint, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=120) as res:
            response = json.load(res)
    except HTTPError as exc:
        raise RuntimeError(f"Ollama HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')}") from exc
    except URLError as exc:
        raise RuntimeError(f"无法连接 Ollama：{exc.reason}；请确认 Ollama 已启动。") from exc
    return response["message"]["content"].strip()
