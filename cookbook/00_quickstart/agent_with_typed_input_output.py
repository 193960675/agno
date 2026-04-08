"""
带类型化输入输出的 Agent - 完整类型安全
======================================
此示例展示了如何为 Agent 定义输入和输出 schema。
你获得端到端类型安全：验证输入、保证输出。

非常适合构建健壮的管道，需要两端都有契约。
Agent 验证输入并保证输出结构。

关键概念：
- input_schema：定义 Agent 接受内容的 Pydantic 模型
- output_schema：定义 Agent 返回内容的 Pydantic 模型
- 传入 dict 或 Pydantic 模型 —— 两者都有效

可以尝试的示例输入：
- {"ticker": "NVDA", "analysis_type": "quick", "include_risks": True}
- {"ticker": "TSLA", "analysis_type": "deep", "include_risks": True}
"""

from typing import List, Literal, Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")


# ---------------------------------------------------------------------------
# 输入 Schema —— Agent 接受的内容
# ---------------------------------------------------------------------------
class AnalysisRequest(BaseModel):
    """请求股票分析的结构化输入。"""

    ticker: str = Field(..., description="股票代码符号（例如：NVDA, AAPL）")
    analysis_type: Literal["quick", "deep"] = Field(
        default="quick",
        description="quick = 仅总结，deep = 包含驱动因素/风险的完整分析",
    )
    include_risks: bool = Field(
        default=True, description="是否包含风险分析"
    )


# ---------------------------------------------------------------------------
# 输出 Schema —— Agent 返回的内容
# ---------------------------------------------------------------------------
class StockAnalysis(BaseModel):
    """股票分析的结构化输出。"""

    ticker: str = Field(..., description="股票代码符号")
    company_name: str = Field(..., description="完整公司名称")
    current_price: float = Field(..., description="当前股价（美元）")
    summary: str = Field(..., description="一句话股票总结")
    key_drivers: Optional[List[str]] = Field(
        None, description="关键增长驱动因素（如深度分析）"
    )
    key_risks: Optional[List[str]] = Field(
        None, description="关键风险（如 include_risks=True）"
    )
    recommendation: str = Field(
        ..., description="以下之一：强力买入、买入、持有、卖出、强力卖出"
    )


# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个生成结构化股票分析的金融 Agent。

## 输入参数

你接收包含以下内容的结构化请求：
- ticker：要分析的股票
- analysis_type："quick"（仅总结）或 "deep"（完整分析）
- include_risks：是否包含风险分析

## 工作流程

1. 获取请求股票的数据
2. 如果 analysis_type 是 "deep"，识别关键驱动因素
3. 如果 include_risks 为 True，识别关键风险
4. 提供明确的推荐

## 规则

- 数据来源：Yahoo Finance
- 输出匹配输入参数 —— "quick" 分析不包含驱动因素
- 推荐必须是以下之一：强力买入、买入、持有、卖出、强力卖出\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_typed_input_output = Agent(
    name="Agent with Typed Input Output",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools(all=True)],
    input_schema=AnalysisRequest,
    output_schema=StockAnalysis,
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
    # 方式 1：以 dict 传入输入
    response_1 = agent_with_typed_input_output.run(
        input={
            "ticker": "NVDA",
            "analysis_type": "deep",
            "include_risks": True,
        }
    )

    # 访问类型化输出
    analysis_1: StockAnalysis = response_1.content

    print(f"\n{'=' * 60}")
    print(f"股票分析：{analysis_1.company_name} ({analysis_1.ticker})")
    print(f"{'=' * 60}")
    print(f"价格：${analysis_1.current_price:.2f}")
    print(f"总结：{analysis_1.summary}")
    if analysis_1.key_drivers:
        print("\n关键驱动因素：")
        for driver in analysis_1.key_drivers:
            print(f"  • {driver}")
    if analysis_1.key_risks:
        print("\n关键风险：")
        for risk in analysis_1.key_risks:
            print(f"  • {risk}")
    print(f"\n推荐：{analysis_1.recommendation}")
    print(f"{'=' * 60}\n")

    # 方式 2：以 Pydantic 模型传入输入
    request = AnalysisRequest(
        ticker="AAPL",
        analysis_type="quick",
        include_risks=False,
    )
    response_2 = agent_with_typed_input_output.run(input=request)

    # 访问类型化输出
    analysis_2: StockAnalysis = response_2.content

    print(f"\n{'=' * 60}")
    print(f"股票分析：{analysis_2.company_name} ({analysis_2.ticker})")
    print(f"{'=' * 60}")
    print(f"价格：${analysis_2.current_price:.2f}")
    print(f"总结：{analysis_2.summary}")
    if analysis_2.key_drivers:
        print("\n关键驱动因素：")
        for driver in analysis_2.key_drivers:
            print(f"  • {driver}")
    if analysis_2.key_risks:
        print("\n关键风险：")
        for risk in analysis_2.key_risks:
            print(f"  • {risk}")
    print(f"\n推荐：{analysis_2.recommendation}")
    print(f"{'=' * 60}\n")

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
类型化输入 + 输出非常适合：

1. API 端点
   @app.post("/analyze")
   def analyze(request: AnalysisRequest) -> StockAnalysis:
       return agent.run(input=request).content

2. 批量处理
   requests = [
       AnalysisRequest(ticker="NVDA", analysis_type="quick"),
       AnalysisRequest(ticker="AMD", analysis_type="quick"),
       AnalysisRequest(ticker="INTC", analysis_type="quick"),
   ]
   results = [agent.run(input=r).content for r in requests]

3. 管道组合
   # Agent 1 的输出是 Agent 2 期望的输入
   screening_result = screener_agent.run(input=criteria).content
   analysis_result = analysis_agent.run(input=screening_result).content

两端类型安全 = 更少错误、更好工具支持、更清晰契约。
"""
