# Aila (v0.1)

本地运行的独立 AI 聊天伙伴原型。当前只包含：人格文件、Ollama 客户端、终端聊天入口。

## 环境

- Windows / Python 3.10+
- 已启动 Ollama，已下载 `qwen3:8b` (`ollama list` 检查)
- 无需额外安装 Python 第三方依赖

## 运行

```powershell
cd E:\AI\Aila
python main.py
```

或双击 `start.bat`。如果模型不叫 `qwen3:8b`，可执行 `python main.py --model qwen3:1.7b`。

命令：`/clear` 清空本次临时上下文；`/exit` 退出。

## 当前边界

- 未实现长期记忆；关闭后不会保留聊天记录
- 未连接 AstrBot / QQ
- 角色是有独立性格的 AI，并非真实人类

## 未来迭代

L2 表达风格测试与改进；L3 长期记忆；L4 知识与背景；L5 学习反馈。
