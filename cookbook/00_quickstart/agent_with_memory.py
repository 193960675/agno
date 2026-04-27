"""
带记忆的 Agent - 记住你的金融 Agent
====================================
此示例展示了如何让 Agent 记住用户偏好。
Agent 能够在所有对话中记住关于你的信息。

与存储（持久化对话历史）不同，记忆持久化用户级别的信息：
偏好、事实、上下文。

关键概念：
- MemoryManager：从对话中提取并存储用户记忆
- enable_agentic_memory：Agent 通过工具调用决定何时存储/召回（高效）
- update_memory_on_run：每次响应后运行记忆管理器（确保捕获）
- user_id：将记忆关联到特定用户

可以尝试的示例提示：
- "我对科技股感兴趣，特别是 AI 公司"
- "我的风险承受能力是中等"
- "你会为我推荐什么股票？"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.tools.yfinance import YFinanceTools
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 记忆管理器配置
# ---------------------------------------------------------------------------

import os
from dotenv import load_dotenv

from agno.models.deepseek import DeepSeek

# Load environment variables from cookbook/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Get the key from environment
key = os.getenv("DEEPSEEK_API_KEY")



memory_manager = MemoryManager(
    model=DeepSeek(id="deepseek-chat", api_key=key),
    db=agent_db,
    additional_instructions="""
    捕获用户喜欢的股票、他们的风险承受能力和投资目标。
    """,
)

# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个金融 Agent —— 一个数据驱动的分析师，获取市场数据、
计算关键比率，并生成简洁、可决策的洞察。

## 记忆

你拥有用户偏好的记忆（自动在上下文中提供）。利用这些来：
- 根据他们的兴趣定制推荐
- 考虑他们的风险承受能力
- 参考他们的投资目标

## 工作流程

1. 获取数据
   - 获取：价格、涨跌幅、市值、P/E、EPS、52周区间
   - 比较时，获取每个股票代码的相同字段

2. 分析
   - 当数据未提供时计算比率（P/E、P/S、利润率）
   - 关键驱动因素和风险 —— 最多 2-3 点
   - 只陈述事实，不猜测

3. 呈现
   - 以一句话总结开头
   - 多股票比较时使用表格
   - 保持简洁

## 规则

- 数据来源：Yahoo Finance。始终注明时间戳。
- 数据缺失？说 "N/A" 并继续。
- 不提供个性化建议 —— 相关时添加免责声明。
- 不使用表情符号。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
user_id = "investor@example.com"

agent_with_memory = Agent(
    name="Agent with Memory",
    model=DeepSeek(id="deepseek-chat", api_key=key),
    instructions=instructions,
    tools=[YFinanceTools(all=True)],
    db=agent_db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 告诉 Agent 关于你的信息
    agent_with_memory.print_response(
        "我对 AI 和半导体股票感兴趣。我的风险承受能力是中等。",
        user_id=user_id,
        stream=True,
    )

    # Agent 现在知道你的偏好
    agent_with_memory.print_response(
        "你会为我推荐什么股票？",
        user_id=user_id,
        stream=True,
    )

    # 查看存储的记忆
    memories = agent_with_memory.get_user_memories(user_id=user_id)
    print("\n" + "=" * 60)
    print("存储的记忆：")
    print("=" * 60)
    pprint(memories)

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
记忆 vs 存储：

- 存储："我们讨论了什么？"（对话历史）
- 记忆："你知道关于我的什么？"（用户偏好）

记忆跨会话持久化：

1. 运行此脚本 —— Agent 学习你的偏好
2. 使用相同的 user_id 开启新会话
3. Agent 仍然记得你喜欢 AI 股票

适用于：
- 个性化推荐
- 记住用户上下文（工作、目标、约束）
- 跨对话建立关系

两种启用记忆的方式：

1. enable_agentic_memory=True（此示例使用）
   - Agent 通过工具调用决定何时存储/召回
   - 更高效 —— 仅在需要时运行

2. update_memory_on_run=True
   - 每次 Agent 响应后运行记忆管理器
   - 确保捕获 —— 不会遗漏用户信息
   - 更高的延迟和成本
"""
