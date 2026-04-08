"""
带状态管理的 Agent - 有自选列表的金融 Agent
==========================================
此示例展示了如何为 Agent 提供可读写修改的持久化状态。
Agent 能够跨对话维护股票自选列表。

与存储（对话历史）和记忆（用户偏好）不同，
状态是 Agent 主动管理的结构化数据：计数器、列表、标志。

关键概念：
- session_state：跨运行持久化的字典
- 工具可通过 run_context.session_state 读/写状态
- 状态变量可通过 {variable_name} 注入到指令中

可以尝试的示例提示：
- "将 NVDA 和 AMD 加入我的自选列表"
- "我的自选列表里有什么？"
- "从列表中移除 AMD"
- "我的自选股票今天表现如何？"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.run import RunContext
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")


# ---------------------------------------------------------------------------
# 修改状态的自定义工具
# ---------------------------------------------------------------------------
def add_to_watchlist(run_context: RunContext, ticker: str) -> str:
    """
    将股票代码添加到自选列表。

    参数：
        ticker: 股票代码符号（例如：NVDA, AAPL）

    返回：
        确认消息
    """
    ticker = ticker.upper().strip()
    watchlist = run_context.session_state.get("watchlist", [])

    if ticker in watchlist:
        return f"{ticker} 已在你的自选列表中"

    watchlist.append(ticker)
    run_context.session_state["watchlist"] = watchlist

    return f"已将 {ticker} 加入自选列表。当前自选列表：{', '.join(watchlist)}"


def remove_from_watchlist(run_context: RunContext, ticker: str) -> str:
    """
    从自选列表中移除股票代码。

    参数：
        ticker: 要移除的股票代码符号

    返回：
        确认消息
    """
    ticker = ticker.upper().strip()
    watchlist = run_context.session_state.get("watchlist", [])

    if ticker not in watchlist:
        return f"{ticker} 不在你的自选列表中"

    watchlist.remove(ticker)
    run_context.session_state["watchlist"] = watchlist

    if watchlist:
        return f"已移除 {ticker}。剩余自选列表：{', '.join(watchlist)}"
    return f"已移除 {ticker}。自选列表现在为空。"


# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个管理股票自选列表的金融 Agent。

## 当前自选列表
{watchlist}

## 能力

1. 管理自选列表
   - 添加股票：使用 add_to_watchlist 工具
   - 移除股票：使用 remove_from_watchlist 工具

2. 获取股票数据
   - 使用 YFinance 工具获取自选股票的价格和指标
   - 比较自选列表中的股票

## 规则

- 始终确认自选列表的变更
- 当被问到"我的股票"或"自选列表"时，参考当前状态
- 报告自选列表表现时获取最新数据\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_state_management = Agent(
    name="Agent with State Management",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        add_to_watchlist,
        remove_from_watchlist,
        YFinanceTools(all=True),
    ],
    session_state={"watchlist": []},
    add_session_state_to_context=True,
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
    # 添加一些股票
    agent_with_state_management.print_response(
        "将 NVDA、AAPL 和 GOOGL 加入我的自选列表",
        stream=True,
    )

    # 查看自选列表
    agent_with_state_management.print_response(
        "我的自选股票今天表现如何？",
        stream=True,
    )

    # 直接查看状态
    print("\n" + "=" * 60)
    print("会话状态：")
    print(
        f"  自选列表: {agent_with_state_management.get_session_state().get('watchlist', [])}"
    )
    print("=" * 60)

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
状态 vs 存储 vs 记忆：

- 状态：Agent 管理的结构化数据（自选列表、计数器、标志）
- 存储：对话历史（"我们讨论了什么？")
- 记忆：用户偏好（"我喜欢什么？")

状态适用于：
- 跟踪项目（自选列表、待办事项、购物车）
- 计数器和进度
- 多步骤工作流
- 任何在对话中变化的结构化数据

访问状态的方式：

1. 在工具中：run_context.session_state["key"]
2. 在指令中：{key}（需设置 add_session_state_to_context=True）
3. 运行后：agent.get_session_state() 或 response.session_state
"""
