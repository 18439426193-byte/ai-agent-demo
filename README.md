# AI Agent 智能问答系统

基于大模型 API 构建的智能问答 Agent，支持多轮对话与 Function Calling 工具调用。

## 功能特点

- 多轮对话：自动维护上下文，支持连续对话
- 工具调用：支持通过 Function Calling 调用外部工具（天气查询）
- 交互式界面：命令行交互，输入即问答

## 技术栈

- Python
- 阿里云百炼（qwen-plus）
- OpenAI SDK

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 在 final_agent.py 中填写你的 API Key
# api_key = "your-api-key-here"

# 3. 运行
python final_agent.py