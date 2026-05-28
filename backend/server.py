"""
LangChain对话助手 - LangServe后端服务
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 将项目根目录添加到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain_core.runnables import RunnableLambda

from backend.config import config
from backend.chains.conversation import (
    create_conversation_chain,
    create_conversation_chain_with_tools,
    create_conversational_chain,
    create_tools_chain,
    get_llm,
)

# 创建FastAPI应用
app = FastAPI(
    title="LangChain Chatbot API",
    description="基于LangChain的智能对话助手API",
    version="1.0.0",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 根路由
@app.get("/")
async def root():
    return {
        "message": "LangChain Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "playground": "/playground",
    }


# 健康检查
@app.get("/health")
async def health():
    return {"status": "healthy"}


# 流式对话Chain
def create_stream_chain():
    """创建支持流式的对话Chain"""
    from langchain_core.output_parsers import StrOutputParser
    from backend.prompts.templates import create_conversation_prompt
    
    prompt = create_conversation_prompt()
    llm = get_llm(provider="dashscope")  # 使用 DashScope（阿里云）
    output_parser = StrOutputParser()
    
    return prompt | llm | output_parser


# 注册路由
# 1. 简单对话
add_routes(
    app,
    create_conversation_chain(),
    path="/chat",
)

# 2. 带工具的对话
add_routes(
    app,
    create_conversation_chain_with_tools(),
    path="/chat/tools",
)

# 3. 流式对话
add_routes(
    app,
    create_stream_chain(),
    path="/chat/stream",
)

# 4. 带记忆的对话
add_routes(
    app,
    create_conversational_chain(),
    path="/chat/history",
)

# 5. 带工具和记忆的完整Chain
add_routes(
    app,
    create_tools_chain(),
    path="/chat/full",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
