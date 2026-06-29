# 🤖 LangChain 智能对话助手

基于 LangChain 框架的现代化智能对话系统，支持多种 LLM 提供商、联网搜索、上下文记忆等功能。

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| 💬 **智能对话** | 自然流畅的语言交互，支持中英文 |
| 🔍 **联网搜索** | 集成 Tavily 搜索，实时获取最新资讯 |
| 🧠 **记忆管理** | 上下文持久化记忆，支持多轮对话 |
| ⚡ **快速响应** | 流式输出，毫秒级智能回复 |
| 🛠️ **工具扩展** | Web 搜索、Wikipedia、计算器等多工具支持 |
| 🔗 **Chain 调用** | LCEL 链式组合，灵活编排 AI 工作流 |

## 🏗️ 项目架构

```
langchain-chatbot/
├── app.py                        # 🌐 独立版 Streamlit 应用（推荐）
├── main.py                       # 旧版单文件应用
├── backend/                      # 🔧 FastAPI + LangServe 后端
│   ├── server.py                 #    FastAPI 服务入口
│   ├── config.py                 #    配置管理
│   ├── chains/                   #    LangChain Chain 定义
│   │   ├── conversation.py       #    对话 Chain
│   │   └── tools.py             #    工具定义
│   └── prompts/                  #    Prompt 模板
│       └── templates.py          #    对话/代码/翻译模板
├── frontend/                     # 🎨 Streamlit 前端
│   └── app.py                    #    前端界面
├── streamlit_cloud_deploy/       # ☁️ Streamlit Cloud 部署版
│   ├── app.py                    #    部署应用
│   └── requirements.txt          #    部署依赖
├── requirements.txt              #   项目依赖
└── .env.example                  #   环境变量模板
```

## 🚀 快速开始

### 方式一：独立版运行（推荐）

最简单的方式，无需启动后端服务：

```bash
# 克隆项目
git clone https://github.com/caster0524/sanyelangchain.git
cd sanyelangchain

# 安装依赖
pip install -r requirements_streamlit.txt

# 配置环境变量（复制 .env.example 为 .env 并填写 API 密钥）
cp .env.example .env

# 运行应用
streamlit run app.py
```

应用将在 **http://localhost:8501** 启动。

### 方式二：前后端分离运行

```bash
# 1. 启动后端服务
cd backend
uvicorn server:app --reload --port 8000

# 2. 启动前端（新终端）
cd frontend
streamlit run app.py
```

后端 API 文档：**http://localhost:8000/docs**

## 🌐 Streamlit Cloud 部署

1. 将 `streamlit_cloud_deploy/` 文件夹内容上传到 GitHub
2. 在 [Streamlit Cloud](https://streamlit.io/cloud) 中创建新应用
3. 在 **Settings → Secrets** 中配置 API 密钥：

```toml
DASHSCOPE_API_KEY = "your-dashscope-api-key"
DASHSCOPE_MODEL = "qwen-plus"
DASHSCOPE_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"
TAVILY_API_KEY = "your-tavily-api-key"
```

## 🔑 API 密钥配置

在 `.env` 文件中配置以下环境变量：

```env
# 阿里云 DashScope（通义千问）- 推荐国内使用
DASHSCOPE_API_KEY=sk-your-key-here
DASHSCOPE_MODEL=qwen-plus

# DeepSeek - 高性价比
Deepseek_API_KEY=sk-your-key-here
DEEPSEEK_MODEL=deepseek-chat

# OpenAI - 国际版
OPENAI_API_KEY=sk-your-key-here

# Tavily 搜索（可选）
TAVILY_API_KEY=tvly-your-key-here

# LangSmith 监控（可选）
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_your-key-here
LANGSMITH_PROJECT=your-project
```

### 获取 API 密钥

| 服务 | 获取地址 |
|------|---------|
| 阿里云 DashScope | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com/) |
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com/) |
| OpenAI | [platform.openai.com](https://platform.openai.com/) |
| Tavily Search | [tavily.com](https://tavily.com/) |
| LangSmith | [smith.langchain.com](https://smith.langchain.com/) |

## 🎯 支持的模型

| 模型 | 提供商 | 特点 |
|------|--------|------|
| `qwen-plus` | DashScope | 国内访问快，中英文优秀 |
| `qwen-max` | DashScope | 旗舰版，推理能力更强 |
| `deepseek-chat` | DeepSeek | 性价比极高 |
| `gpt-4o-mini` | OpenAI | 综合能力强 |

## 🛠️ 可用工具

| 工具 | 功能 |
|------|------|
| 🌐 Tavily Search | 联网搜索最新信息 |
| 📚 Wikipedia | 百科知识查询 |
| 🧮 Calculator | 数学计算 |

## 📡 后端 API 端点

| 端点 | 说明 |
|------|------|
| `GET /` | API 信息 |
| `GET /health` | 健康检查 |
| `POST /chat/stream` | 简单对话 |
| `POST /chat/tools/stream` | 带工具对话 |
| `POST /chat/history/stream` | 带记忆对话 |
| `POST /chat/full/stream` | 完整功能（工具+记忆） |

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| **AI 框架** | LangChain + LangServe |
| **前端** | Streamlit |
| **后端** | FastAPI + Uvicorn |
| **支持 LLM** | DashScope / DeepSeek / OpenAI |
| **搜索** | Tavily / Wikipedia / DuckDuckGo |
| **监控** | LangSmith |

## 📋 项目依赖

```txt
langchain>=0.3.0
langchain-core>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
langserve>=0.3.0
fastapi>=0.115.0
streamlit>=1.40.0
python-dotenv>=1.0.0
```

## 📄 License

MIT License

---

**Made with ❤️ using LangChain & Streamlit**
