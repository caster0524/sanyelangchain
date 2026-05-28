"""
LangChain对话助手 - Prompt模板
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage


# 系统提示词
SYSTEM_PROMPT = """你是一个友善、智能的对话助手，由LangChain驱动。

你的能力：
- 能够进行自然流畅的对话交流
- 可以帮助你回答问题、提供建议
- 支持中英文对话
- 能够记住对话上下文

请保持回答简洁、友好、有帮助。如果不知道答案，请如实说明。"""


def create_conversation_prompt() -> ChatPromptTemplate:
    """
    创建对话Prompt模板
    
    包含：
    - System Message：系统提示
    - History：历史消息
    - Input：当前用户输入
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])


def create_code_assistant_prompt() -> ChatPromptTemplate:
    """代码助手Prompt"""
    code_system = """你是一个专业的编程助手，擅长：
    - 解答编程问题
    - 代码审查和优化建议
    - 调试帮助
    - 技术解释
    
    请用清晰的方式解释代码，用中文回答。"""
    
    return ChatPromptTemplate.from_messages([
        ("system", code_system),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])


def create_translator_prompt() -> ChatPromptTemplate:
    """翻译助手Prompt"""
    translator_system = """你是一个专业的翻译助手，可以：
    - 中英文互译
    - 保持原文语气和风格
    - 提供多种翻译版本供参考
    
    请给出准确的翻译，并简要解释翻译选择的原因。"""
    
    return ChatPromptTemplate.from_messages([
        ("system", translator_system),
        MessagesPlaceholder(variable_name="history", optional=True),
        ("human", "{input}"),
    ])
