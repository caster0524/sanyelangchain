# LangChain Chatbot - Streamlit Cloud 部署指南

## 项目结构

```
streamlit_cloud_deploy/
├── app.py                      # 主应用文件
├── requirements.txt             # 依赖文件
└── .streamlit/
    └── config.toml             # Streamlit 配置
```

## 部署步骤

### 1. 上传代码到 GitHub

将 `streamlit_cloud_deploy` 文件夹内的所有文件上传到 GitHub 仓库：
- `app.py`
- `requirements.txt`
- `.streamlit/config.toml`

### 2. 配置 Streamlit Secrets

在 Streamlit Cloud 上部署时，需要在 **Settings → Secrets** 中添加以下配置：

```toml
# 阿里云 DashScope API（推荐使用）
DASHSCOPE_API_KEY = "your-dashscope-api-key"
DASHSCOPE_MODEL = "qwen-plus"
DASHSCOPE_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 或者使用 DeepSeek API
DEEPSEEK_API_KEY = "your-deepseek-api-key"
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

# 或者使用 OpenAI API
OPENAI_API_KEY = "your-openai-api-key"
OPENAI_MODEL = "gpt-4o-mini"

# 可选：Tavily 搜索 API
TAVILY_API_KEY = "your-tavily-api-key"
```

### 3. 部署到 Streamlit Cloud

1. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
2. 点击 "New app"
3. 选择你的 GitHub 仓库和分支
4. 设置主文件路径为 `streamlit_cloud_deploy/app.py`
5. 点击 "Deploy!"

## 功能特性

- 💬 **智能对话** - 基于 LangChain 的自然语言交互
- 🔍 **联网搜索** - 集成 Tavily 搜索获取实时信息
- 🧠 **记忆管理** - 支持上下文记忆和会话管理
- ⚡ **快速响应** - 流式输出，毫秒级响应

## 支持的模型

1. **阿里云 DashScope（通义千问）** - 推荐，国内访问速度快
2. **DeepSeek** - 性价比高
3. **OpenAI GPT** - 国际版

## 注意事项

- 确保 API 密钥已正确配置在 Streamlit Secrets 中
- Tavily API 为可选功能，可不配置
- 应用默认使用 DashScope 模型

## 本地运行

```bash
cd streamlit_cloud_deploy
pip install -r requirements.txt
streamlit run app.py
```

## 获取 API 密钥

- **阿里云 DashScope**: https://dashscope.console.aliyun.com/
- **DeepSeek**: https://platform.deepseek.com/
- **OpenAI**: https://platform.openai.com/
- **Tavily**: https://tavily.com/
