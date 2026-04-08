"""
顺序工作流 - 股票研究管道
========================
此示例展示了如何创建带有顺序步骤的工作流。
每个步骤由专门 Agent 处理，输出流向下一步。

与团队（Agent 动态协作）不同，工作流让你
对执行顺序和数据流有明确的控制。

关键概念：
- Workflow：编排步骤序列
- Step：用特定任务包装 Agent
- 步骤按顺序执行，每步建立在前面基础上

可以尝试的示例提示：
- "分析 NVDA"
- "研究特斯拉用于投资"
- "给我一份 Apple 的报告"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.workflow import Step, Workflow

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
workflow_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 步骤 1：数据收集器 —— 获取原始市场数据
# ---------------------------------------------------------------------------
data_agent = Agent(
    name="Data Gatherer",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools(all=True)],
    instructions="""\
你是一个数据收集 Agent。你的工作是获取全面的市场数据。

对于请求的股票，收集：
- 当前价格和日涨跌
- 市值和成交量
- P/E 比率、EPS 和其他关键比率
- 52周最高和最低
- 近期价格趋势

清晰地呈现原始数据。不要分析 —— 只收集和组织。\
""",
    db=workflow_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

data_step = Step(
    name="Data Gathering",
    agent=data_agent,
    description="获取股票的全面市场数据",
)

# ---------------------------------------------------------------------------
# 步骤 2：分析师 —— 解释数据
# ---------------------------------------------------------------------------
analyst_agent = Agent(
    name="Analyst",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions="""\
你是一个金融分析师。你接收数据团队的原始市场数据。

你的工作是：
- 解释关键指标（P/E 对于此行业是高还是低？）
- 识别优势和劣势
- 注意任何警示信号或积极信号
- 与典型行业基准比较

提供分析，而非推荐。要客观和数据驱动。\
""",
    db=workflow_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

analysis_step = Step(
    name="Analysis",
    agent=analyst_agent,
    description="分析市场数据并识别关键洞察",
)

# ---------------------------------------------------------------------------
# 步骤 3：报告撰写者 —— 产生最终输出
# ---------------------------------------------------------------------------
report_agent = Agent(
    name="Report Writer",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions="""\
你是一个报告撰写者。你接收研究团队的分析。

你的工作是：
- 将分析综合为清晰的投资简报
- 以一句话总结开头
- 包含推荐（买入/持有/卖出）及理由
- 保持简洁 —— 最多 200 字
- 结尾用小表格展示关键指标

为忙碌的投资者撰写，他们想要快速看到结论。\
""",
    db=workflow_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

report_step = Step(
    name="Report Writing",
    agent=report_agent,
    description="生成简洁的投资简报",
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
sequential_workflow = Workflow(
    name="Sequential Workflow",
    description="三步研究管道：数据 → 分析 → 报告",
    steps=[
        data_step,  # 步骤 1：收集数据
        analysis_step,  # 步骤 2：分析数据
        report_step,  # 步骤 3：撰写报告
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sequential_workflow.print_response(
        "分析 NVIDIA (NVDA) 用于投资",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
工作流 vs 团队：

- 工作流：明确的步骤顺序、可预测执行、清晰数据流
- 团队：动态协作、领导者决定谁做什么

使用工作流当：
- 步骤必须按特定顺序发生
- 每步有清晰、专门的职责
- 你想要可预测、可重复的执行
- 步骤 N 的输出流入步骤 N+1

使用团队当：
- Agent 需要动态协作
- 领导者应该决定涉及谁
- 任务受益于来回讨论

高级工作流功能（未在此展示）：
- Parallel：并行运行步骤
- Condition：仅在满足条件时运行步骤
- Loop：重复步骤直到条件满足
- Router：动态选择运行哪个步骤
"""
