"""
带工具的 Agent - 金融 Agent
============================
你的第一个 Agno Agent：一个数据驱动的金融分析师，能够获取市场数据、
计算关键指标，并提供简洁的洞察。

此示例展示了如何给 Agent 赋予工具以与外部数据源交互。
Agent 使用 YFinanceTools 来获取实时市场数据。

可以尝试的示例提示：
- "AAPL 的当前价格是多少？"
- "比较 NVDA 和 AMD —— 哪个看起来更强？"
- "给我一份微软的快速投资简报"
- "特斯拉的 P/E 比率是多少？与行业相比如何？"
- "显示 FAANG 股票的关键指标"
"""

import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

from libs.agno.agno.models.deepseek.deepseek import DeepSeek
from libs.agno.agno.tools.decorator import tool
from libs.agno.agno.tools.hackernews import HackerNewsTools

# Load environment variables from cookbook/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Get the key from environment
key = os.getenv("DEEPSEEK_API_KEY")
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
- 不使用表情符号。\
"""

ins2 = '''
你是专业的 **agno 学习与使用专属导师**，精通agno的所有功能、安装、配置、命令、实操场景与排错。
无论我提出任何与agno相关的问题，你都必须遵循以下规则进行精准教学与解答：

1. 回答范围：只专注于agno相关内容，包括但不限于：安装部署、基础使用、命令语法、功能模块、配置文件、项目实操、报错排查、进阶用法、最佳实践等。
2. 回答原则：
   - 精准无误，不编造信息；
   - 从我的知识水平出发，由浅入深讲解；
   - 步骤清晰、可直接照着操作；
   - 必要时提供代码/命令示例与解释。
3. 输出结构：
   - 先给出核心结论；
   - 再分步讲解原理或操作步骤；
   - 补充示例与注意事项；
   - 如涉及复杂内容，使用结构化排版（列表、代码块、重点标注）。
4. 扩展支持：
   - 若问题涉及多个知识点，自动梳理知识体系；
   - 主动提示常见误区、易错点；
   - 可根据我的需求调整讲解深度（入门/进阶/高阶）。

请全程以教学者身份，耐心、完整、可落地地教会我使用agno，确保我能理解并独立操作。'''

@tool(name='获取天气', description='查询输入城市的天气')
def get_weather(city: str):
    return f'{city}天气暴风雨'

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_tools = Agent(
    name="Agent with Tools",
    model=DeepSeek(id="deepseek-chat", api_key=key),
    instructions=ins2,
    tools=[],
    add_datetime_to_context=True,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_with_tools.print_response(
        "获取一些Hacker News的热门技术讨论", stream=True
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
可以尝试这些提示：

1. 单股票分析
   "Apple 的当前估值是多少？是否昂贵？"

2. 比较
   "比较 Google 和 Microsoft 作为投资选择"

3. 行业概览
   "显示顶级 AI 股票的关键指标：NVDA, AMD, GOOGL, MSFT"

4. 快速查看
   "特斯拉今天的股价是多少？"

5. 深度分析
   "分析 Amazon 的财务状况 —— 收入、利润率和增长"
"""
