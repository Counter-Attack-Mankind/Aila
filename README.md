# Aila v0.2 — 本地知识库

独立的 AI 聊天核心，不依赖 AstrBot。AstrBot 未来只作为收发消息的适配层。

## 环境与启动

- Windows / Python 3.10+，不需要额外 Python 依赖
- Ollama 已安装、运行，并准备好 `qwen3:8b`

```powershell
python main.py
```

或双击 `start.bat`。可以使用 `python main.py --model qwen3:8b --kaomoji-rate 0` 禁止程序注入颜文字候选。

命令：`/clear` 清空临时对话，重载 L1/L2；`/debug` 显示检索命中与注入信息；`/exit` 退出。

## 知识库

- `knowledge/origin.json`：名字和动画背景（已确认资料）
- `knowledge/creator.json`：公开的创造关系与未知边界
- `knowledge/kaomoji.json`：按情绪提供候选，默认仅有 15% 概率提供，不保证模型一定使用

这是小规模关键词检索，暂不支持复杂的语义理解。简单的相邻轮次指代可继承上轮话题。知识提示只用于当前轮，不进入聊天历史。模型仍可能出现幻觉。

注意：**仓库是公开的**。不要把真实个人隐私写进上述 JSON 并提交到 GitHub。未来私人资料应放入本地 `data/` 下，并实现访问控制。`visibility` 字段只有 public 检索过滤作用，不等于认证或完整权限管理。

## 测试

```powershell
python -m unittest discover -s tests -v
```

## 暂不实现

长期记忆、AstrBot 插件、LoRA 训练和向量数据库。原 L1 v1.5、L2 v1.3 保持不变。
