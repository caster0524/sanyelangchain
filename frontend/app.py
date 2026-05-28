"""
LangChain对话助手 - Streamlit前端
精美的对话界面，支持流式输出
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 页面配置
st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主色调 */
    :root {
        --primary-color: #4F46E5;
        --secondary-color: #818CF8;
        --background-color: #0F172A;
        --card-background: #1E293B;
        --text-color: #F8FAFC;
        --muted-color: #94A3B8;
    }
    
    /* 全局样式 */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* 标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    /* 聊天消息 */
    .user-message {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        color: #F8FAFC;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* 聊天容器 */
    .chat-container {
        border-radius: 16px;
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* 侧边栏样式 */
    .sidebar-section {
        background: rgba(51, 65, 85, 0.5);
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5, #6366F1);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6366F1, #818CF8);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
    }
    
    /* 状态指示器 */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background: #10B981;
        box-shadow: 0 0 10px #10B981;
    }
    
    .status-offline {
        background: #EF4444;
        box-shadow: 0 0 10px #EF4444;
    }
    
    /* 模型信息卡片 */
    .model-info {
        background: rgba(79, 70, 229, 0.1);
        border-left: 3px solid #4F46E5;
        padding: 12px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    
    /* 工具标签 */
    .tool-tag {
        display: inline-block;
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 4px 4px 4px 0;
    }
</style>
""", unsafe_allow_html=True)


# 后端配置
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def init_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    if "chain_type" not in st.session_state:
        st.session_state.chain_type = "simple"
    if "is_connected" not in st.session_state:
        st.session_state.is_connected = False


def check_backend_connection():
    """检查后端连接状态"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def stream_chat(endpoint: str, message: str, session_id: str = None):
    """流式调用聊天API"""
    url = f"{BACKEND_URL}{endpoint}"
    
    # 根据endpoint决定是否需要session_id
    needs_session = endpoint in ["/chat/history/stream", "/chat/full/stream"]
    
    payload = {"input": message}
    if needs_session and session_id:
        payload["config"] = {"configurable": {"session_id": session_id}}
    
    try:
        with requests.post(url, json=payload, stream=True, timeout=60) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        decoded = line.decode('utf-8')
                        if decoded.startswith('data:'):
                            data = decoded[5:].strip()
                            if data and data != '[DONE]':
                                try:
                                    yield json.loads(data)
                                except:
                                    yield {"content": data}
                        else:
                            yield {"content": decoded}
            else:
                yield {"error": f"请求失败: {response.status_code}"}
    except Exception as e:
        yield {"error": str(e)}


def call_chat_api(endpoint: str, message: str, session_id: str = None):
    """非流式调用聊天API"""
    url = f"{BACKEND_URL}{endpoint}"
    
    needs_session = endpoint in ["/chat/history/invoke", "/chat/full/invoke"]
    
    payload = {"input": message}
    if needs_session and session_id:
        payload["config"] = {"configurable": {"session_id": session_id}}
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result.get("output", result.get("content", str(result)))
        else:
            return f"❌ 请求失败: {response.status_code}"
    except Exception as e:
        return f"❌ 连接失败: {str(e)}"


def render_message(role: str, content: str):
    """渲染单条消息"""
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>👤 你</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 助手</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)


def main():
    """主界面"""
    init_session_state()
    
    # 标题
    st.markdown('<h1 class="main-title">🤖 LangChain 智能对话助手</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## ⚙️ 设置")
        
        # 连接状态
        is_connected = check_backend_connection()
        st.session_state.is_connected = is_connected
        
        status_color = "status-online" if is_connected else "status-offline"
        status_text = "在线" if is_connected else "离线"
        st.markdown(
            f'<span class="status-indicator {status_color}"></span>'
            f'<span>后端服务: {status_text}</span>',
            unsafe_allow_html=True
        )
        
        if not is_connected:
            st.warning("⚠️ 后端服务未连接，请先启动后端:\n\n"
                      "```bash\ncd backend\nuvicorn server:app --reload\n```")
        
        st.divider()
        
        # Chain类型选择
        st.markdown("### 🔗 Chain类型")
        chain_options = {
            "simple": "💬 简单对话",
            "tools": "🛠️ 带工具对话", 
            "history": "💾 带记忆对话",
            "full": "🎯 完整功能"
        }
        
        selected_chain = st.selectbox(
            "选择对话模式",
            options=list(chain_options.keys()),
            format_func=lambda x: chain_options[x],
            index=list(chain_options.keys()).index(st.session_state.chain_type)
        )
        st.session_state.chain_type = selected_chain
        
        st.divider()
        
        # 模型信息
        st.markdown("### 📊 模型信息")
        st.markdown("""
        <div class="model-info">
            <strong>模型:</strong> GPT-4o-mini<br>
            <strong>温度:</strong> 0.7<br>
            <strong>流式输出:</strong> ✓
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # 可用工具
        st.markdown("### 🛠️ 可用工具")
        tools_list = ["🌐 Web搜索", "📚 Wikipedia", "🧮 计算器"]
        for tool in tools_list:
            st.markdown(f'<span class="tool-tag">{tool}</span>', unsafe_allow_html=True)
        
        st.divider()
        
        # 清空对话
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # 显示session_id
        st.caption(f"Session: {st.session_state.session_id}")
    
    # 聊天区域
    chat_endpoint_map = {
        "simple": "/chat/stream",
        "tools": "/chat/tools/stream",
        "history": "/chat/history/stream",
        "full": "/chat/full/stream"
    }
    
    endpoint = chat_endpoint_map[st.session_state.chain_type]
    
    # 显示历史消息
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            render_message(msg["role"], msg["content"])
    
    # 欢迎消息
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; color: #94A3B8;">
            <h2>👋 欢迎使用 LangChain 对话助手</h2>
            <p>基于LangChain框架开发，支持多种对话模式</p>
            <p style="margin-top: 20px;">
                <span class="tool-tag">💬 智能对话</span>
                <span class="tool-tag">🛠️ 工具调用</span>
                <span class="tool-tag">💾 上下文记忆</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 输入区域
    st.divider()
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "💬 输入消息...",
            placeholder="输入你的问题，按Enter发送",
            key="user_input",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.button("发送 ✈️", use_container_width=True)
    
    # 处理发送
    if (user_input or send_button) and user_input:
        # 添加用户消息
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # 清空输入
        st.session_state.user_input = ""
        
        # 添加助手消息占位
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # 流式输出
            if st.session_state.is_connected:
                try:
                    for chunk in stream_chat(
                        endpoint, 
                        user_input, 
                        st.session_state.session_id
                    ):
                        if "error" in chunk:
                            full_response = chunk["error"]
                            break
                        content = chunk.get("content", "")
                        if content:
                            full_response += content
                            message_placeholder.markdown(full_response + "▌")
                    
                    # 移除光标
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f"❌ 发生错误: {str(e)}"
                    message_placeholder.markdown(full_response)
            else:
                # 本地模拟（后端未启动时）
                full_response = call_llm_fallback(user_input)
                message_placeholder.markdown(full_response)
        
        # 保存助手回复
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
        
        # 重新渲染
        st.rerun()


def call_llm_fallback(message: str) -> str:
    """当后端不可用时的本地模拟响应"""
    responses = [
        f"后端服务未连接。请先启动后端服务。\n\n你发送的消息是: {message}",
        f"我收到了你的消息: {message}\n\n后端服务未启动，无法处理请求。",
    ]
    import random
    return random.choice(responses)


if __name__ == "__main__":
    main()
