"""
LangChain Chatbot - Streamlit Cloud 部署版
单文件完整应用，可直接部署到 Streamlit Community Cloud
"""

import os
import sys
import streamlit as st
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# 加载.env文件（本地开发），Streamlit Cloud上使用Secrets
load_dotenv()

# ==================== 配置 ====================
def get_config(key, default=""):
    """从环境变量或Streamlit Secrets读取配置"""
    env_val = os.getenv(key, "")
    if env_val:
        return env_val
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

DEEPSEEK_API_KEY = get_config("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = get_config("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_API_BASE = get_config("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

DASHSCOPE_API_KEY = get_config("DASHSCOPE_API_KEY", "")
DASHSCOPE_MODEL = get_config("DASHSCOPE_MODEL", "qwen-plus")
DASHSCOPE_API_BASE = get_config("DASHSCOPE_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")

OPENAI_API_KEY = get_config("OPENAI_API_KEY", "")
OPENAI_MODEL = get_config("OPENAI_MODEL", "gpt-4o-mini")

LANGSMITH_API_KEY = get_config("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = get_config("LANGSMITH_PROJECT", "rengong241")

TAVILY_API_KEY = get_config("TAVILY_API_KEY", "")

DEFAULT_LLM = get_config("DEFAULT_LLM", "dashscope")

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="🤖 ChatAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 样式 ====================
st.markdown("""
<style>
    :root {
        --primary: #6366F1;
        --primary-light: #818CF8;
        --primary-dark: #4F46E5;
        --secondary: #EC4899;
        --accent: #06B6D4;
        --bg-dark: #0F172A;
        --bg-card: #1E293B;
        --bg-surface: #334155;
        --text-primary: #F8FAFC;
        --text-muted: #94A3B8;
        --text-dim: #64748B;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --border: rgba(255, 255, 255, 0.1);
        --shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 20px 60px rgba(0, 0, 0, 0.4);
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #1a1f35 50%, var(--bg-card) 100%);
        min-height: 100vh;
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .subtitle {
        text-align: center;
        color: var(--text-muted);
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    .user-bubble {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary));
        color: white;
        border-radius: 20px 20px 6px 20px;
        padding: 16px 20px;
        margin: 12px 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.35);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .user-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.45);
    }

    .assistant-bubble {
        background: linear-gradient(135deg, var(--bg-surface), var(--bg-card));
        color: var(--text-primary);
        border-radius: 20px 20px 20px 6px;
        padding: 16px 20px;
        margin: 12px 0;
        max-width: 75%;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
        border: 1px solid var(--border);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .assistant-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
    }

    .avatar {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        margin-right: 10px;
        font-size: 1rem;
        flex-shrink: 0;
    }

    .user-avatar {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
    }

    .assistant-avatar {
        background: linear-gradient(135deg, var(--accent), var(--primary));
    }

    .message-content {
        display: inline-block;
        vertical-align: top;
        line-height: 1.6;
    }

    .feature-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.05));
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px 16px;
        text-align: center;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
    }

    .feature-icon { font-size: 2.5rem; margin-bottom: 12px; }
    .feature-title { font-weight: 600; color: var(--text-primary); font-size: 1rem; margin-bottom: 8px; }
    .feature-desc { color: var(--text-muted); font-size: 0.85rem; line-height: 1.5; }

    .tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 4px 6px 4px 0;
        transition: transform 0.2s ease;
    }

    .tag-success { background: rgba(16, 185, 129, 0.15); color: var(--success); }
    .tag-info { background: rgba(59, 130, 246, 0.15); color: #60A5FA; }
    .tag-warning { background: rgba(245, 158, 11, 0.15); color: var(--warning); }
    .tag:hover { transform: scale(1.05); }

    .sidebar-section {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        border: 1px solid var(--border);
    }

    .sidebar-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .status-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 12px;
    }

    .status-dot {
        width: 10px;
        height: 10px;
        background: var(--success);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    .status-text { font-size: 0.9rem; color: var(--success); font-weight: 500; }
    .status-model { font-size: 0.85rem; color: var(--text-muted); }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.1); }
    }

    .stButton button {
        width: 100%;
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        border: none;
    }

    .stButton button:hover { transform: translateY(-2px); }
    .stButton button:active { transform: translateY(0); }

    .stTextInput > div > div > input {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 14px 20px;
        color: var(--text-primary);
        font-size: 1rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }

    .stTextInput > div > div > input::placeholder { color: var(--text-dim); }

    .stToggle > label > div:first-child {
        background: var(--bg-surface);
        border-radius: 12px;
    }

    .stToggle > label > div:first-child > div {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
    }

    .stDivider { border-color: var(--border); margin: 24px 0; }

    .stDeployButton { display: none !important; }
    footer { display: none !important; }
    #MainMenu { display: none !important; }
    .stToolbar { display: none !important; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb { background: var(--bg-surface); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-fadeInUp { animation: fadeInUp 0.5s ease forwards; }

    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .user-bubble, .assistant-bubble { max-width: 90%; }
    }
</style>
""", unsafe_allow_html=True)


# ==================== 搜索功能 ====================
def web_search(query):
    try:
        from langchain_community.tools import TavilySearchResults

        if not TAVILY_API_KEY:
            return None

        os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
        search_tool = TavilySearchResults(max_results=5)
        results = search_tool.invoke({"query": query})

        if results:
            search_info = "【搜索结果】\n\n"
            for i, result in enumerate(results, 1):
                search_info += f"{i}. **{result.get('title', '')}**\n"
                search_info += f"{result.get('content', '')}\n"
                search_info += f"来源: {result.get('url', '')}\n\n"
            return search_info
        return None
    except Exception as e:
        st.warning(f"搜索失败: {e}")
        return None


# ==================== LangChain 集成 ====================
def get_llm():
    try:
        from langchain_openai import ChatOpenAI

        if DASHSCOPE_API_KEY:
            return ChatOpenAI(
                api_key=DASHSCOPE_API_KEY,
                base_url=DASHSCOPE_API_BASE,
                model=DASHSCOPE_MODEL,
                temperature=0.7
            )
        elif DEEPSEEK_API_KEY:
            return ChatOpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_API_BASE,
                model=DEEPSEEK_MODEL,
                temperature=0.7
            )
        elif OPENAI_API_KEY:
            return ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model=OPENAI_MODEL,
                temperature=0.7
            )
        else:
            return None
    except Exception as e:
        st.error(f"LLM初始化失败: {e}")
        return None


def get_langchain_chain():
    try:
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.chat_history import InMemoryChatMessageHistory
        from langchain_core.runnables.history import RunnableWithMessageHistory

        llm = get_llm()
        if llm is None:
            return None

        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个友善、智能的AI助手。

你的能力：
- 能够进行自然流畅的对话交流
- 可以帮助用户回答问题、提供建议
- 支持中英文对话
- 能够记住对话上下文

如果有搜索信息，请结合搜索结果进行回答。

请保持回答简洁、友好、有帮助。如果不知道答案，请如实说明。"""),
            MessagesPlaceholder(variable_name="history", optional=True),
            ("human", "{input}"),
        ])

        chain = prompt | llm | StrOutputParser()

        store = {}

        def get_history(session_id):
            if session_id not in store:
                store[session_id] = InMemoryChatMessageHistory()
            return store[session_id]

        return RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
    except Exception as e:
        st.error(f"LangChain初始化失败: {e}")
        return None


def invoke_chain(chain, message, session_id, search_info=""):
    try:
        config = {"configurable": {"session_id": session_id}}

        if search_info:
            full_message = f"{message}\n\n{search_info}"
        else:
            full_message = message

        result = chain.invoke({"input": full_message}, config)

        if isinstance(result, dict) and "output" in result:
            return result["output"]
        return str(result)
    except Exception as e:
        return f"错误: {str(e)}"


# ==================== 会话状态 ====================
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "use_search" not in st.session_state:
        st.session_state.use_search = False


# ==================== 渲染函数 ====================
def render_message(role, content):
    if role == "user":
        st.markdown(f'''
        <div class="user-bubble animate-fadeInUp">
            <span class="avatar user-avatar">👤</span>
            <span class="message-content">{content}</span>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="assistant-bubble animate-fadeInUp">
            <span class="avatar assistant-avatar">🤖</span>
            <span class="message-content">{content}</span>
        </div>
        ''', unsafe_allow_html=True)


def render_welcome():
    st.markdown('<h1 class="main-title">🤖 ChatAI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">智能对话助手 · 让AI触手可及</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    features = [
        ("💬", "智能对话", "自然流畅的语言交互体验"),
        ("🔍", "联网搜索", "实时获取最新资讯"),
        ("🧠", "记忆管理", "上下文持久化记忆"),
        ("⚡", "快速响应", "毫秒级智能回复"),
    ]

    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f'''
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            ''', unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="text-align: center; color: var(--text-muted); font-size: 0.95rem;">
        开始与 AI 对话，体验智能交互的魅力 🚀
    </div>
    """, unsafe_allow_html=True)


# ==================== 主程序 ====================
def main():
    init_session()

    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-title">⚙️ 设置</div>', unsafe_allow_html=True)

        has_api = bool(DEEPSEEK_API_KEY or DASHSCOPE_API_KEY or OPENAI_API_KEY)
        model_name = "DeepSeek" if DEEPSEEK_API_KEY else ("DashScope" if DASHSCOPE_API_KEY else ("OpenAI" if OPENAI_API_KEY else "未配置"))

        st.markdown(f'''
        <div class="status-container">
            <span class="status-dot"></span>
            <div>
                <div class="status-text">模型: {model_name}</div>
                <div class="status-model">{DASHSCOPE_MODEL if DASHSCOPE_API_KEY else (DEEPSEEK_MODEL if DEEPSEEK_API_KEY else OPENAI_MODEL)}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if not has_api:
            st.warning("⚠️ 请配置 API 密钥")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-title">🔍 搜索功能</div>', unsafe_allow_html=True)

        st.session_state.use_search = st.toggle(
            "启用联网搜索",
            value=st.session_state.use_search,
            disabled=not TAVILY_API_KEY
        )

        if TAVILY_API_KEY:
            st.markdown('<span class="tag tag-info">🔍 Tavily 搜索已配置</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="tag tag-warning">⚠️ 搜索未配置</span>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-title">✨ 功能特性</div>', unsafe_allow_html=True)

        features = [
            ("💬", "智能对话"),
            ("💾", "上下文记忆"),
            ("🔗", "Chain调用"),
            ("📤", "快速响应"),
        ]

        for icon, name in features:
            st.markdown(f'<span class="tag tag-success">{icon} {name}</span>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)

        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chain = None
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'''
        <div style="text-align: center; padding-top: 16px;">
            <span style="color: var(--text-dim); font-size: 0.8rem;">
                Session: {st.session_state.session_id[:12]}...
            </span>
        </div>
        ''', unsafe_allow_html=True)

    user_input = st.text_input(
        "",
        placeholder="💬 输入消息，按 Enter 发送...",
        key="chat_input",
        label_visibility="collapsed"
    )

    if st.button("🚀", use_container_width=True) and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.to_process = user_input

    if "to_process" in st.session_state and st.session_state.to_process:
        current_msg = st.session_state.to_process
        st.session_state.to_process = None

        if not st.session_state.chain and has_api:
            with st.spinner("🔧 初始化 AI..."):
                st.session_state.chain = get_langchain_chain()

        search_info = ""
        if st.session_state.use_search and TAVILY_API_KEY:
            with st.spinner("🔍 正在搜索..."):
                search_info = web_search(current_msg)

        with st.spinner("🤖 思考中..."):
            if st.session_state.chain:
                response = invoke_chain(
                    st.session_state.chain,
                    current_msg,
                    st.session_state.session_id,
                    search_info
                )
            else:
                response = """⚠️ **AI未初始化**

请配置 API 密钥后重试。"""

        st.session_state.messages.append({"role": "assistant", "content": response})

    main_content = st.container()
    with main_content:
        if not st.session_state.messages:
            render_welcome()

        for msg in st.session_state.messages:
            render_message(msg["role"], msg["content"])

    st.divider()


if __name__ == "__main__":
    main()