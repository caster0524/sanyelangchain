"""
LangChain对话助手 - 对话Chain定义
使用LangChain Expression Language (LCEL)
"""

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from backend.config import config


def get_llm(model: str = None, provider: str = None):
    """
    获取LLM实例
    
    Args:
        model: 模型名称，可选
        provider: 提供商，可选 deepseek / dashscope / openai，默认从config读取
    """
    provider = provider or config.DEFAULT_LLM
    
    if provider == "deepseek" and config.DEEPSEEK_API_KEY:
        return ChatOpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_API_BASE,
            model=model or config.DEEPSEEK_MODEL,
            temperature=0.7,
            streaming=True,
        )
    elif provider == "dashscope" and config.DASHSCOPE_API_KEY:
        return ChatOpenAI(
            api_key=config.DASHSCOPE_API_KEY,
            base_url=config.DASHSCOPE_API_BASE,
            model=model or config.DASHSCOPE_MODEL,
            temperature=0.7,
            streaming=True,
        )
    elif config.OPENAI_API_KEY:
        return ChatOpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_API_BASE,
            model=model or config.OPENAI_MODEL,
            temperature=0.7,
            streaming=True,
        )
    else:
        raise ValueError("未配置任何LLM API密钥")


def create_base_chain(provider: str = None):
    """创建基础对话Chain（无记忆）"""
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个友善、智能的AI助手，由LangChain驱动。

你的能力：
- 能够进行自然流畅的对话交流
- 可以帮助回答问题、提供建议
- 支持中英文对话
- 能够记住对话上下文

请保持回答简洁、友好、有帮助。如果不知道答案，请如实说明。"""),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])
    
    llm = get_llm(provider=provider)
    output_parser = StrOutputParser()
    
    return prompt | llm | output_parser


def create_conversation_chain(provider: str = None):
    """创建对话Chain（无记忆）"""
    return create_base_chain(provider)


def create_conversation_chain_with_tools(provider: str = None):
    """创建带工具的对话Chain"""
    from backend.chains.tools import tools
    
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个友善、智能的AI助手，由LangChain驱动。

当你需要查找实时信息、计算数学题或查询百科知识时，可以使用工具。
其他时候直接回答即可。"""),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])
    
    llm = get_llm(provider=provider).bind_tools(tools)
    output_parser = StrOutputParser()
    
    return prompt | llm | output_parser


def create_conversational_chain(provider: str = None):
    """创建带记忆的对话Chain"""
    base_chain = create_base_chain(provider)
    
    # 会话历史存储
    store = {}
    
    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]
    
    return RunnableWithMessageHistory(
        base_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


def create_tools_chain(provider: str = None):
    """创建带工具和记忆的完整Chain"""
    from backend.chains.tools import tools
    
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个友善、智能的AI助手，由LangChain驱动。

当你需要查找实时信息、计算数学题或查询百科知识时，可以使用工具。
其他时候直接回答即可。"""),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])
    
    llm = get_llm(provider=provider).bind_tools(tools)
    output_parser = StrOutputParser()
    
    base_chain = prompt | llm | output_parser
    
    # 会话历史存储
    store = {}
    
    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]
    
    return RunnableWithMessageHistory(
        base_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
