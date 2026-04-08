"""
人机协作 - 执行前确认
====================
此示例展示了如何在执行某些工具前要求用户确认。
对于不可逆或敏感操作至关重要。

我们将基于自学习 Agent 构建，在保存学习内容前请求用户确认。

关键概念：
- @tool(requires_confirmation=True)：标记需要批准的工具
- run_response.active_requirements：检查待处理确认
- requirement.confirm() / requirement.reject()：批准或拒绝
- agent.continue_run()：决策后继续执行

一些实际应用：
- 执行前确认敏感操作
- 调用前审查 API 调用
- 验证数据转换
- 批准关键系统中的自动化操作

可以尝试的示例提示：
- "科技股的良好 P/E 比率是多少？保存那个洞察。"
- "分析 NVDA 并保存任何洞察"
- "我们保存了什么学习内容？"
"""

import json
from datetime import datetime, timezone

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.text_reader import TextReader
from agno.models.google import Gemini
from agno.tools import tool
from agno.tools.yfinance import YFinanceTools
from agno.utils import pprint
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType
from rich.console import Console
from rich.prompt import Prompt

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 学习内容的知识库
# ---------------------------------------------------------------------------
learnings_kb = Knowledge(
    name="Agent Learnings HITL",
    vector_db=ChromaDb(
        name="learnings",
        collection="learnings",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    max_results=5,
    contents_db=agent_db,
)


# ---------------------------------------------------------------------------
# 自定义工具：保存学习内容（需要确认）
# ---------------------------------------------------------------------------
@tool(requires_confirmation=True)
def save_learning(title: str, learning: str) -> str:
    """
    将可复用的洞察保存到知识库以供将来参考。
    此操作需要用户确认后才执行。

    参数：
        title: 简短描述性标题（例如："科技股 P/E 基准")
        learning: 要保存的洞察 —— 具体且可操作

    返回：
        确认消息
    """
    if not title or not title.strip():
        return "无法保存：标题必填"
    if not learning or not learning.strip():
        return "无法保存：学习内容必填"

    payload = {
        "title": title.strip(),
        "learning": learning.strip(),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }

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
你是一个能够随时间学习和改进的金融 Agent。

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

3. 保存有价值的洞察
   - 如果发现可复用的内容，用 save_learning 保存
   - 用户会在保存前被要求确认
   - 好的学习内容是具体、可操作、可复用的

## 什么是好的学习内容

- 具体："科技股 P/E 比率通常在 20-35x" 而非 "P/E 变化"
- 可操作：可应用于未来问题
- 可复用：超出此对话范围有用

不要保存：原始数据、一次性事实或显而易见的信息。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
human_in_the_loop_agent = Agent(
    name="Agent with Human in the Loop",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        YFinanceTools(all=True),
        save_learning,
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
    console = Console()

    # 提问可能触发保存
    run_response = human_in_the_loop_agent.run(
        "科技股的健康 P/E 比率是多少？保存那个洞察。"
    )

    # 打印初始响应内容（实际答案）
    if run_response.content:
        pprint.pprint_run_response(run_response)

    # 处理任何确认要求
    if run_response.active_requirements:
        for requirement in run_response.active_requirements:
            if requirement.needs_confirmation:
                console.print(
                    f"\n[bold yellow]需要确认[/bold yellow]\n"
                    f"工具: [bold blue]{requirement.tool_execution.tool_name}[/bold blue]\n"
                    f"参数: {requirement.tool_execution.tool_args}"
                )

                choice = (
                    Prompt.ask(
                        "你想继续吗？",
                        choices=["y", "n"],
                        default="y",
                    )
                    .strip()
                    .lower()
                )

                if choice == "n":
                    requirement.reject()
                    console.print("[red]已拒绝[/red]")
                else:
                    requirement.confirm()
                    console.print("[green]已批准[/green]")

        # 用用户决策继续运行
        run_response = human_in_the_loop_agent.continue_run(
            run_id=run_response.run_id,
            requirements=run_response.requirements,
        )

        # 工具执行后打印最终响应
        pprint.pprint_run_response(run_response)

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
人机协作模式：

1. 敏感操作确认
   @tool(requires_confirmation=True)
   def delete_file(path: str) -> str:
       ...

2. 外部调用确认
   @tool(requires_confirmation=True)
   def send_email(to: str, subject: str, body: str) -> str:
       ...

3. 金融交易确认
   @tool(requires_confirmation=True)
   def place_order(ticker: str, quantity: int, side: str) -> str:
       ...

模式：
1. 用 @tool(requires_confirmation=True) 标记工具
2. 用 agent.run() 运行 Agent
3. 遍历 run_response.active_requirements
4. 检查 requirement.needs_confirmation
5. 调用 requirement.confirm() 或 requirement.reject()
6. 用 requirements 调用 agent.continue_run()

这让你完全控制哪些操作被执行。
"""
