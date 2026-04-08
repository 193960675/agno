"""
带存储的 Agent - 有持久化存储的金融 Agent
==========================================
在 01 的金融 Agent 基础上，此示例添加了持久化存储。
你的 Agent 现在能够跨运行记住对话。

询问 NVDA，关闭脚本，稍后回来 —— 从上次中断的地方继续。
对话历史保存到 SQLite 并自动恢复。

关键概念：
- Run：每次运行 Agent（通过 agent.print_response() 或 agent.run()）
- Session：对话线程，由 session_id 标识
- 相同的 session_id = 连续对话，即使跨运行

可以尝试的示例提示：
- "AAPL 的当前价格是多少？"
- "与 Microsoft 比较"（它会记住 AAPL）
- "根据我们的讨论，哪个看起来更好？"
- "我们到目前为止分析了哪些股票？"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个金融 Agent —— 一个数据驱动的分析师，获取市场数据、
计算关键比率，并生成简洁、可决策的洞察。

## 工作流程

1. 明确需求
   - 从公司名称识别股票代码（例如：Apple → AAPL）
   - 如果有歧义，询问用户

2. 获取数据
   - 获取：价格、涨跌幅、市值、P/E、EPS、52周区间
   - 比较时，获取每个股票代码的相同字段

3. 分析
   - 当数据未提供时计算比率（P/E、P/S、利润率）
   - 关键驱动因素和风险 —— 最多 2-3 点
   - 只陈述事实，不猜测

4. 呈现
   - 以一句话总结开头
   - 多股票比较时使用表格
   - 保持简洁

## 规则

- 数据来源：Yahoo Finance。始终注明时间戳。
- 数据缺失？说 "N/A" 并继续。
- 不提供个性化建议 —— 相关时添加免责声明。
- 不使用表情符号。
- 相关时引用之前的分析。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_storage = Agent(
    name="Agent with Storage",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools(all=True)],
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
    # 使用一致的 session_id 来跨运行持久化对话
    # 注意：如果未设置，session_id 会自动生成
    session_id = "finance-agent-session"

    # 第一轮：分析一只股票
    agent_with_storage.print_response(
        "给我一份 NVIDIA 的快速投资简报",
        session_id=session_id,
        stream=True,
    )

    # 第二轮：比较 —— Agent 记住了第一轮的 NVDA
    agent_with_storage.print_response(
        "与特斯拉比较",
        session_id=session_id,
        stream=True,
    )

    # 第三轮：根据完整对话请求推荐
    agent_with_storage.print_response(
        "根据我们的讨论，哪个看起来是更好的投资？",
        session_id=session_id,
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
尝试这个流程：

1. 运行脚本 —— 它分析 NVDA，与 TSLA 比较，然后推荐
2. 注释掉上面的三个提示
3. 添加：agent.print_response("AMD 怎么样？", session_id=session_id, stream=True)
4. 再次运行 —— 它记住完整的 NVDA vs TSLA 对话

存储层将你的对话历史持久化到 SQLite。
随时重启脚本并从中断处继续。
"""
