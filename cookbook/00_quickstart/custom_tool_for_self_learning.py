"""
自定义工具用于自学习 - 编写自己的工具
======================================
此示例展示了如何为 Agent 编写自定义工具。
工具只是一个 Python 函数 —— Agent 在需要时调用它。

我们将构建一个可以保存洞察到知识库的自学习 Agent。
关键概念：任何函数都可以成为工具。

关键概念：
- 工具是带有 docstring 的 Python 函数（docstring 告知 Agent 工具做什么）
- Agent 根据对话决定何时调用你的工具
- 返回字符串将结果传达给 Agent

可以尝试的示例提示：
- "科技股的良好 P/E 比率是多少？保存那个洞察。"
- "记住 NVDA 的数据中心收入是关键增长驱动因素"
- "我们保存了什么学习内容？"
"""

import json
from datetime import datetime, timezone

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.reader.text_reader import TextReader
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 学习内容的知识库
# ---------------------------------------------------------------------------
learnings_kb = Knowledge(
    name="Agent Learnings",
    vector_db=ChromaDb(
        name="learnings",
        collection="learnings",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        hybrid_rrf_k=60,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    max_results=5,
    contents_db=agent_db,
)


# ---------------------------------------------------------------------------
# 自定义工具：保存学习内容
# ---------------------------------------------------------------------------
def save_learning(title: str, learning: str) -> str:
    """
    将可复用的洞察保存到知识库以供将来参考。

    参数：
        title: 简短描述性标题（例如："科技股 P/E 基准")
        learning: 要保存的洞察 —— 具体且可操作

    返回：
        确认消息
    """
    # 验证输入
    if not title or not title.strip():
        return "无法保存：标题必填"
    if not learning or not learning.strip():
        return "无法保存：学习内容必填"

    # 构建数据
    payload = {
        "title": title.strip(),
        "learning": learning.strip(),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }

    # 保存到知识库
    learnings_kb.insert(
        name=payload["title"],
        text_content=json.dumps(payload, ensure_ascii=False),
        reader=TextReader(),
        skip_if_exists=True,
    )

    return f"已保存：'{title}'"


# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个能够学习和改进的金融 Agent。

你有两项特殊能力：
1. 搜索知识库查找之前保存的学习内容
2. 使用 save_learning 工具保存新的洞察

## 工作流程

1. 首先检查知识库
   - 回答前，搜索相关的先前学习内容
   - 将相关洞察应用到你的响应中

2. 收集信息
   - 使用 YFinance 工具获取市场数据
   - 结合知识库洞察

3. 提议学习内容
   - 回答后，考虑：是否有可复用的洞察？
   - 如果有，用此格式提议：

---
**提议的学习内容**

标题：[简洁标题]
学习：[洞察 —— 具体且可操作]

保存吗？（是/否）
---

- 只有在用户说"是"后才调用 save_learning
- 如果用户说"否"，确认并继续

## 什么是好的学习内容

- 具体："科技股 P/E 比率通常在 20-35x" 而非 "P/E 变化"
- 可操作：可应用于未来问题
- 可复用：超出此对话范围有用

不要保存：原始数据、一次性事实或显而易见的信息。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
self_learning_agent = Agent(
    name="Self-Learning Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        YFinanceTools(all=True),
        save_learning,  # 我们的自定义工具 —— 就是一个 Python 函数！
    ],
    knowledge=learnings_kb,
    search_knowledge=True,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 提问可能产生学习内容
    self_learning_agent.print_response(
        "科技股的健康 P/E 比率是多少？",
        stream=True,
    )

    # 如果 Agent 提议了学习内容，批准它
    self_learning_agent.print_response(
        "是",
        stream=True,
    )

    # 之后，Agent 可以召回学习内容
    self_learning_agent.print_response(
        "我们保存了什么学习内容？",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
编写自定义工具：

1. 定义一个带类型提示和 docstring 的函数
   def my_tool(param: str) -> str:
       '''描述此工具做什么。

       参数：
           param: 此参数的作用

       返回：
           工具返回什么
       '''
       # 你的逻辑
       return "结果"

2. 添加到 Agent 的工具列表
   agent = Agent(
       tools=[my_tool],
       ...
   )

docstring 是关键 —— 它告知 Agent：
- 工具做什么
- 需要什么参数
- 返回什么

Agent 使用这些信息决定何时及如何调用你的工具。
"""
