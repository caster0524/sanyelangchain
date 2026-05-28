"""
LangChain对话助手 - 单文件完整版
可直接运行，集成了前端和后端逻辑
"""

import os
import streamlit as st
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ==================== 配置 ====================
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="🤖 LangChain Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS ====================
st.markdown("""
<style>
    /* 主 题 */
    :root {
        --primary: #6366F1;
        --primary-dark: #4F46E5;
        --bg-dark: #0F172A;
        --bg-card: #1E293B;
        --text-primary: #F8FAFC;
        --text-muted: #94A3B8;
        --success: #10B981;
        --error: #EF4444;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #1a1f35 50%, var(--bg-card) 100%);
    }
    
    /* 标题渐变 */
    .gradient-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366F1, #818CF8, #A78BFA, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1rem 0 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .gradient-subtitle {
        text-align: center;
        color: var(--text-muted);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* 消息气泡 */
    .user-bubble {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary));
        color: white;
        border-radius: 20px 20px 4px 20px;
        padding: 14px 18px;
        margin: 10px 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.35);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .assistant-bubble {
        background: linear-gradient(135deg, #334155, #475569);
        color: var(--text-primary);
        border-radius: 20px 20px 20px 4px;
        padding: 14px 18px;
        margin: 10px 0;
        max-width: 75%;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .avatar-user::before { content: "👤"; margin-right: 8px; }
    .avatar-assistant::before { content: "🤖"; margin-right: 8px; }
    
    /* 功能卡片 */
    .feature-card {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.25);
    }
    
    .feature-icon { font-size: 2.5rem; margin-bottom: 12px; }
    .feature-title { font-weight: 600; margin-bottom: 8px; color: var(--text-primary); }
    .feature-desc { color: var(--text-muted); font-size: 0.85rem; }
    
    /* 状态指示器 */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-online {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-offline {
        background: rgba(239, 68, 68, 0.15);
        color: var(--error);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .status-online .status-dot { background: var(--success); }
    .status-offline .status-dot { background: var(--error); }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* 侧边栏 */
    .sidebar-section {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 14px;
        padding: 18px;
        margin: 14px 0;
        border: 1px solid rgba(148, 163, 184, 0.08);
    }
    
    .sidebar-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 14px;
    }
    
    /* 工具标签 */
    .tool-tag {
        display: inline-block;
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 4px 4px 4px 0;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    /* 模式选择卡片 */
    .mode-card {
        background: rgba(51, 65, 85, 0.5);
        border-radius: 12px;
        padding: 14px;
        cursor: pointer;
        border: 2px solid transparent;
        transition: all 0.25s ease;
        margin: 8px 0;
    }
    
    .mode-card:hover {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .mode-card.selected {
        background: rgba(99, 102, 241, 0.15);
        border-color: var(--primary);
    }
    
    .mode-title { font-weight: 600; margin-bottom: 4px; }
    .mode-desc { font-size: 0.8rem; color: var(--text-muted); }
    
    /* 隐藏元素 */
    .stDeployButton { display: none !important; }
    footer { display: none !important; }
    #MainMenu { display: none !important; }
    
    /* 聊天容器 */
    .chat-wrapper {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* 输入框 */
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 14px 18px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 会话状态 ====================
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    if "chain_mode" not in st.session_state:
        st.session_state.chain_mode = "full"
    if "is_connected" not in st.session_state:
        st.session_state.is_connected = False


# ==================== API调用 ====================
def check_connection():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return r.status_code == 200
    except:
        return False


def get_endpoint(mode: str) -> str:
    endpoints = {
        "simple": "/chat/stream",
        "tools": "/chat/tools/stream",
        "history": "/chat/history/stream",
        "full": "/chat/full/stream"
    }
    return endpoints.get(mode, "/chat/stream")


def chat_stream(message: str, mode: str, session_id: str):
    """流式聊天"""
    endpoint = get_endpoint(mode)
    url = f"{BACKEND_URL}{endpoint}"
    
    needs_session = mode in ["history", "full"]
    payload = {"input": message}
    if needs_session:
        payload["config"] = {"configurable": {"session_id": session_id}}
    
    try:
        with requests.post(url, json=payload, stream=True, timeout=120) as resp:
            if resp.status_code == 200:
                for line in resp.iter_lines():
                    if line:
                        decoded = line.decode('utf-8')
                        if decoded.startswith('data:'):
                            data = decoded[5:].strip()
                            if data and data != '[DONE]':
                                try:
                                    yield json.loads(data).get("content", "")
                                except:
                                    yield data
                        else:
                            yield decoded
            else:
                yield f"[错误] HTTP {resp.status_code}"
    except Exception as e:
        yield f"[连接错误] {str(e)}"


# ==================== 渲染函数 ====================
def render_message(role: str, content: str):
    """渲染消息"""
    if role == "user":
        st.markdown(f'<div class="user-bubble"><span class="avatar-user"></span>{content}</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-bubble"><span class="avatar-assistant"></span>{content}</div>', 
                   unsafe_allow_html=True)


def render_welcome():
    """欢迎界面"""
    st.markdown('<h1 class="gradient-title">LangChain 智能助手</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subtitle">基于 LangChain 框架的现代化对话系统</p>', unsafe_allow_html=True)
    
    # 功能卡片
    cols = st.columns(4)
    features = [
        ("💬", "智能对话", "自然语言交互"),
        ("🔗", "Chain调用", "LCEL链式组合"),
        ("🛠️", "工具扩展", "Web搜索/计算"),
        ("💾", "记忆管理", "上下文持久化"),
    ]
    
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()


def render_sidebar():
    """侧边栏"""
    with st.sidebar:
        st.markdown("## ⚙️ 控制面板")
        
        # 连接状态
        is_connected = check_connection()
        st.session_state.is_connected = is_connected
        
        status_class = "status-online" if is_connected else "status-offline"
        status_text = "已连接" if is_connected else "未连接"
        st.markdown(f"""
        <div class="status-badge {status_class}">
            <span class="status-dot"></span>
            后端服务: {status_text}
        </div>
        """, unsafe_allow_html=True)
        
        if not is_connected:
            st.warning("⚠️ 请先启动后端服务")
            with st.expander("📝 启动说明"):
                st.code("cd backend\nuvicorn server:app --reload --port 8000", language="bash")
        
        st.divider()
        
        # 模式选择
        st.markdown('<div class="sidebar-title">对话模式</div>', unsafe_allow_html=True)
        
        modes = [
            ("full", "🎯", "完整功能", "工具+记忆+流式输出"),
            ("simple", "💬", "简单对话", "基础LLM调用"),
            ("tools", "🛠️", "工具模式", "Web搜索+计算器"),
            ("history", "💾", "记忆模式", "上下文连续对话"),
        ]
        
        for mode_id, icon, title, desc in modes:
            selected = st.session_state.chain_mode == mode_id
            css_class = "mode-card selected" if selected else "mode-card"
            
            if st.button(f"{icon} {title}\n`{desc}`", key=f"mode_{mode_id}", use_container_width=True):
                st.session_state.chain_mode = mode_id
                st.rerun()
            
            st.markdown(f'<div class="{css_class}"></div>', unsafe_allow_html=True)
        
        st.divider()
        
        # 工具信息
        st.markdown('<div class="sidebar-title">可用工具</div>', unsafe_allow_html=True)
        tools_list = ["🌐 Web搜索", "📚 Wikipedia", "🧮 计算器"]
        for t in tools_list:
            st.markdown(f'<span class="tool-tag">{t}</span>', unsafe_allow_html=True)
        
        st.divider()
        
        # 操作按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 清空", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("🔄 重置", use_container_width=True):
                st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                st.session_state.messages = []
                st.rerun()
        
        # Session信息
        st.caption(f"Session ID: `{st.session_state.session_id[:20]}...`")


# ==================== 主程序 ====================
def main():
    init_session()
    render_sidebar()
    
    # 欢迎界面（无消息时）
    if not st.session_state.messages:
        render_welcome()
    
    # 消息历史
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            render_message(msg["role"], msg["content"])
    
    # 输入区域
    st.divider()
    
    # 快捷问题
    st.markdown("**💡 试试这些：**")
    quick_questions = [
        "解释一下什么是LangChain",
        "用Python写一个快速排序",
        "今天有什么新闻？",
        "帮我计算: 1234 * 5678"
    ]
    
    cols = st.columns(4)
    for col, q in zip(cols, quick_questions):
        with col:
            if st.button(q, key=f"quick_{q[:10]}", use_container_width=True):
                st.session_state.quick_input = q
    
    # 输入框
    user_input = st.text_input(
        "💬 输入你的问题...",
        value=st.session_state.get("quick_input", ""),
        placeholder="输入消息后按 Enter 发送...",
        key="main_input"
    )
    
    # 发送按钮
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        send = st.button("🚀 发送", key="main_send", use_container_width=True)
    with col2:
        clear = st.button("🗑️ 清空", key="main_clear", use_container_width=True)
    
    # 处理清空
    if clear:
        st.session_state.messages = []
        st.rerun()
    
    # 处理发送
    if send and user_input:
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.quick_input = ""
        
        # 助手回复
        with st.spinner("🤖 AI正在思考..."):
            response_placeholder = st.empty()
            full_response = ""
            
            # 调用API
            if st.session_state.is_connected:
                for chunk in chat_stream(user_input, st.session_state.chain_mode, st.session_state.session_id):
                    if chunk:
                        full_response += chunk
                        response_placeholder.markdown(f'<div class="assistant-bubble"><span class="avatar-assistant"></span>{full_response}▌</div>', 
                                                     unsafe_allow_html=True)
                
                # 移除光标
                if full_response:
                    response_placeholder.markdown(f'<div class="assistant-bubble"><span class="avatar-assistant"></span>{full_response}</div>', 
                                                 unsafe_allow_html=True)
            else:
                # 后端未连接时显示提示
                full_response = f"""⚠️ **后端服务未连接**
                
请先启动后端服务：
```bash
cd backend
uvicorn server:app --reload --port 8000
```

或者使用独立版本直接运行：
```bash
python main.py
```

---
你发送的消息：`{user_input}`"""
                response_placeholder.markdown(f'<div class="assistant-bubble"><span class="avatar-assistant"></span>{full_response}</div>', 
                                             unsafe_allow_html=True)
        
        # 保存助手回复
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        st.rerun()


if __name__ == "__main__":
    main()
