"""
多智能体团队 - 投资研究团队
==========================
此示例展示了如何创建协同工作的 Agent 团队。
每个 Agent 有专门的角色，团队领导者协调。

我们将构建一个具有对立视角的投资研究团队：
- 牛方 Agent：阐述投资的理由
- 空方 Agent：阐述反对投资的理由
- 主分析师：综合为平衡的推荐

这种对抗方法比单个 Agent 产生更好的分析。

关键概念：
- Team：由领导者协调的 Agent 组
- Members：具有独特角色的专门 Agent
- 领导者委派、综合并产生最终输出

可以尝试的示例提示：
- "我应该投资 NVIDIA 吗？"
- "分析特斯拉作为长期投资"
- "Apple 目前是否估值过高？"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.team.team import Team
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
team_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 牛方 Agent —— 阐述投资的理由
# ---------------------------------------------------------------------------
bull_agent = Agent(
    name="Bull Analyst",
    role="阐述股票的投资理由",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools(all=True)],
    db=team_db,
    instructions="""\
你是牛方分析师。你的工作是尽可能有力地阐述
投资某股票的理由。找到积极因素：
- 增长驱动因素和催化剂
- 竞争优势
- 强劲的财务和指标
- 市场机会

要有说服力但基于数据。使用工具获取真实数字。\
""",
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

# ---------------------------------------------------------------------------
# 空方 Agent —— 阐述反对投资的理由
# ---------------------------------------------------------------------------
bear_agent = Agent(
    name="Bear Analyst",
    role="阐述反对股票投资的理由",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools(all=True)],
    db=team_db,
    instructions="""\
你是空方分析师。你的工作是尽可能有力地阐述
反对投资某股票的理由。找到风险：
- 估值担忧
- 竞争威胁
- 财务薄弱点
- 市场或宏观风险

要批判但公正。使用工具获取真实数字支持你的担忧。\
""",
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
multi_agent_team = Team(
    name="Multi-Agent Team",
    model=Gemini(id="gemini-3-flash-preview"),
    members=[bull_agent, bear_agent],
    instructions="""\
你领导一个投资研究团队，包含牛方分析师和空方分析师。

## 流程

1. 将股票发送给两位分析师
2. 让每位独立阐述理由
3. 将他们的论点综合为平衡的推荐

## 输出格式

听取两位分析师后，提供：
- **牛方论点总结**：牛方分析师的关键观点
- **空方论点总结**：空方分析师的关键观点
- **综合**：他们在哪里同意？在哪里不同意？
- **推荐**：你的平衡观点（买入/持有/卖出）及置信度
- **关键指标**：重要数字的表格

要果断但承认不确定性。\
""",
    db=team_db,
    show_members_responses=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 第一次分析
    multi_agent_team.print_response(
        "我应该投资 NVIDIA (NVDA) 吗？",
        stream=True,
    )

    # 后续问题 —— 团队记住之前的分析
    multi_agent_team.print_response(
        "AMD 与之相比如何？",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
何时使用团队 vs 单个 Agent：

单个 Agent：
- 一个连贯的任务
- 不需要对立观点
- 简单更好

团队：
- 需要多重视角
- 专门专业知识
- 情益于分工的复杂任务
- 对对抗推理（如本示例）

其他团队模式：

1. 研究 → 分析 → 写作管道
   researcher = Agent(role="收集信息")
   analyst = Agent(role="分析数据")
   writer = Agent(role="撰写报告")

2. 检查者模式
   worker = Agent(role="完成任务")
   checker = Agent(role="验证工作")

3. 专家路由
   classifier = Agent(role="路由到专家")
   specialists = [finance_agent, legal_agent, tech_agent]
"""
