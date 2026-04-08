"""
带结构化输出的 Agent - 有类型化响应的金融 Agent
==============================================
此示例展示了如何从 Agent 获取结构化、类型化的响应。
不是自由格式的文本，而是获得一个可信赖的 Pydantic 模型。

非常适合构建管道、UI 或集成，需要可预测的数据结构。
解析、存储、显示 —— 不需要正则表达式。

关键概念：
- output_schema：定义响应结构的 Pydantic 模型
- Agent 的响应始终匹配此 schema
- 通过 response.content 访问结构化数据

可以尝试的示例提示：
- "分析 NVDA"
- "给我一份特斯拉的报告"
- "Apple 的投资理由是什么？"
"""

from typing import List, Optional

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
# 结构化输出 Schema
# ---------------------------------------------------------------------------
class StockAnalysis(BaseModel):
    """股票分析的结构化输出。"""

    ticker: str = Field(..., description="股票代码符号（例如：NVDA）")
    company_name: str = Field(..., description="完整公司名称")
    current_price: float = Field(..., description="当前股价（美元）")
    market_cap: str = Field(..., description="市值（例如：'3.2T' 或 '150B')")
    pe_ratio: Optional[float] = Field(None, description="P/E 比率，如可用")
    week_52_high: float = Field(..., description="52周最高价")
    week_52_low: float = Field(..., description="52周最低价")
    summary: str = Field(..., description="一句话股票总结")
    key_drivers: List[str] = Field(..., description="2-3 个关键增长驱动因素")
    key_risks: List[str] = Field(..., description="2-3 个关键风险")
    recommendation: str = Field(
        ..., description="以下之一：强力买入、买入、持有、卖出、强力卖出"
    )


# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个金融 Agent —— 一个数据驱动的分析师，获取市场数据、
计算关键比率，并生成简洁、可决策的洞察。

## 工作流程

1. 获取数据
   - 获取：价格、涨跌幅、市值、P/E、EPS、52周区间
   - 获取分析所需的所有字段

2. 分析
   - 识别 2-3 个关键驱动因素（什么在起作用）
   - 识别 2-3 个关键风险（可能出什么问题）
   - 只陈述事实，不猜测

3. 推荐
   - 根据数据，提供明确的推荐
   - 要果断但注明这不是个性化建议

## 规则

- 数据来源：Yahoo Finance
- 数据缺失？可选字段用 null，必填字段估算
- 推荐必须是以下之一：强力买入、买入、持有、卖出、强力卖出\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_structured_output = Agent(
    name="Agent with Structured Output",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools(all=True)],
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
    # 获取结构化输出
    response = agent_with_structured_output.run("分析 NVIDIA")

    # 访问类型化数据
    analysis: StockAnalysis = response.content

    # 编程使用
    print(f"\n{'=' * 60}")
    print(f"股票分析：{analysis.company_name} ({analysis.ticker})")
    print(f"{'=' * 60}")
    print(f"价格：${analysis.current_price:.2f}")
    print(f"市值：{analysis.market_cap}")
    print(f"P/E 比率：{analysis.pe_ratio or 'N/A'}")
    print(f"52周区间：${analysis.week_52_low:.2f} - ${analysis.week_52_high:.2f}")
    print(f"\n总结：{analysis.summary}")
    print("\n关键驱动因素：")
    for driver in analysis.key_drivers:
        print(f"  • {driver}")
    print("\n关键风险：")
    for risk in analysis.key_risks:
        print(f"  • {risk}")
    print(f"\n推荐：{analysis.recommendation}")
    print(f"{'=' * 60}\n")

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
结构化输出非常适合：

1. 构建 UI
   analysis = agent.run("分析 TSLA").content
   render_stock_card(analysis)

2. 存入数据库
   db.insert("analyses", analysis.model_dump())

3. 比较股票
   nvda = agent.run("分析 NVDA").content
   amd = agent.run("分析 AMD").content
   if nvda.pe_ratio < amd.pe_ratio:
       print(f"{nvda.ticker} 的 P/E 更低")

4. 构建管道
   tickers = ["AAPL", "GOOGL", "MSFT"]
   analyses = [agent.run(f"分析 {t}").content for t in tickers]

Schema 保证你始终获得期望的字段。
无需解析，无意外。
"""
