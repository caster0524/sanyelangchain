"""
LangChain对话助手 - 工具定义
"""

from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun


# 搜索工具
@tool
def search_web(query: str) -> str:
    """
    搜索互联网获取最新信息。
    
    适用于：
    - 查询实时新闻、天气、股价
    - 查找不确定的事实
    - 获取最新发布的信息
    
    Args:
        query: 搜索关键词
        
    Returns:
        搜索结果摘要
    """
    search = DuckDuckGoSearchRun()
    results = search.invoke(query)
    return results


# Wikipedia搜索工具
@tool
def search_wikipedia(query: str) -> str:
    """
    在Wikipedia上搜索词条信息。
    
    适用于：
    - 查询百科知识
    - 获取概念定义
    - 了解人物、地点、事件
    
    Args:
        query: 搜索词条
        
    Returns:
        词条摘要
    """
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    return wikipedia.invoke(query)


# 计算器工具
@tool
def calculator(expression: str) -> str:
    """
    进行数学计算。
    
    适用于：
    - 算术运算
    - 百分比计算
    - 简单数学问题
    
    Args:
        expression: 数学表达式，如 "2+2", "100*5"
        
    Returns:
        计算结果
    """
    try:
        # 安全计算（仅支持基本运算）
        allowed_chars = set("0123456789+-*/.() ")
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"计算结果：{expression} = {result}"
        else:
            return "❌ 表达式包含不允许的字符"
    except Exception as e:
        return f"❌ 计算错误：{str(e)}"


# 工具列表
tools = [search_web, search_wikipedia, calculator]
