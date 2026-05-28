"""
LangChain对话助手 - 后端配置
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置"""
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.getenv("Deepseek_API_KEY", "")
    DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # 阿里云DashScope配置（通义千问）
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
    DASHSCOPE_API_BASE = os.getenv("DASHSCOPE_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen-plus")
    
    # OpenAI配置（备用）
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # LangSmith监控配置
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "langchain-chatbot")
    
    # 其他API
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    
    # 服务配置
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # 默认使用的LLM提供商
    DEFAULT_LLM = os.getenv("DEFAULT_LLM", "deepseek")  # deepseek / dashscope / openai


config = Config()
